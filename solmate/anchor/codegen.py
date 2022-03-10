import os
import re
import subprocess
from functools import partial
from typing import Dict, Iterable, Set, Union, Callable, Literal, Optional

from pod import Vec
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID
from solana.sysvar import SYSVAR_RENT_PUBKEY
from spl.token.constants import TOKEN_PROGRAM_ID

from .editor import CodeEditor
from .idl import (
    Idl,
    IdlTypeDefinition,
    IdlTypeDefinitionTy,
    IdlType,
    EnumFields,
    IdlAccountItem,
    IdlInstruction,
)
from solmate.utils import camel_to_snake, pascal_to_snake, snake_to_pascal


class CodeGen:
    idl: Idl
    program_id: Union[PublicKey, str]
    root_module: str
    source_path: str
    external_types: Dict[str, Callable]
    default_accounts: Dict[str, Union[PublicKey, str, Callable]]
    instr_tag_values: Literal["incremental", "anchor"]
    accnt_tag_values: Optional[Literal["incremental", "anchor"]]

    _editors: Dict[str, CodeEditor]
    _all_defined_types: Set[str]  # all type names for this module
    _defined_types: Set[str]  # all type names for which code is generated
    _expected_types: Set[str]  # all type names used somewhere in this module
    _package_editor: CodeEditor

    def __init__(
        self,
        idl,
        program_id,
        root_module,
        source_path,
        external_types: Dict[str, Callable[[CodeEditor], str]] = None,
        default_accounts=None,
        instr_tag_values="incremental",
        accnt_tag_values="incremental",
        skip_types=None,
    ):
        self.idl = idl
        self.program_id = program_id
        self.root_module = root_module
        self.source_path = source_path
        self.instr_tag_values = instr_tag_values  # type: ignore
        self.accnt_tag_values = accnt_tag_values  # type: ignore

        if external_types is None:
            self.external_types = dict()
        else:
            self.external_types = external_types

        if default_accounts is None:
            self.default_accounts = dict()
        else:
            self.default_accounts = {
                camel_to_snake(name): val for name, val in default_accounts.items()
            }

        if skip_types is None:
            self.skip_types = []
        else:
            self.skip_types = skip_types

        self._editors = {}
        self._defined_types = set()
        self._expected_types = set()
        self._all_defined_types = set()
        for type_def in self._get_type_definitions():
            self._all_defined_types.add(type_def.name)

    def _get_editor(self, name, is_file=True) -> CodeEditor:
        if name not in self._editors:
            subpath = name.replace(".", "/")
            if not is_file:
                subpath += "/__init__"
            subpath += ".py"

            fullpath = os.path.join(self.source_path, subpath)
            self._editors[name] = CodeEditor(fullpath)
            self._editors[name].load()

        return self._editors[name]

    @staticmethod
    def _add_packing_methods(editor, is_struct):
        # this allows IDE's to give better autocomplete for these methods
        # (otherwise, there is no need to add these.)
        if is_struct:
            pass
            # editor.add_lines(
            #     "\n",
            #     "    @classmethod\n",
            #     "    def _to_bytes_partial(cls, buffer, obj):\n",
            #     "        # to modify packing, change this method\n",
            #     "        return super()._to_bytes_partial(buffer, obj)\n",
            #     "\n",
            #     "    @classmethod\n",
            #     "    def _from_bytes_partial(cls, buffer):\n",
            #     "        # to modify unpacking, change this method\n",
            #     "        return super()._from_bytes_partial(buffer)\n",
            # )
        else:
            editor.add_lines(
                "\n",
                "    @classmethod\n",
                "    def _to_bytes_partial(cls, buffer, obj, **kwargs):\n",
                "        # to modify packing, change this method\n",
                "        return super()._to_bytes_partial(buffer, obj, **kwargs)\n",
                "\n",
                "    @classmethod\n",
                "    def _from_bytes_partial(cls, buffer, **kwargs):\n",
                "        # to modify unpacking, change this method\n",
                "        return super()._from_bytes_partial(buffer, **kwargs)\n",
            )

        editor.add_lines(
            "\n" "    @classmethod\n",
            "    def to_bytes(cls, obj, **kwargs):\n",
            '        return cls.pack(obj, converter="bytes", **kwargs)\n',
            "\n",
            "    @classmethod\n",
            "    def from_bytes(cls, raw, **kwargs):\n",
            '        return cls.unpack(raw, converter="bytes", **kwargs)\n',
        )

    def _get_type_as_string(
        self, field_type, editor, within_types, explicit_forward_ref=False
    ):
        if field_type.is_a(IdlType.BOOL):
            return "bool"
        elif field_type <= IdlType.I128:
            editor.add_from_import("pod", field_type.get_name())
            return field_type.get_name()
        elif field_type.is_a(IdlType.BYTES):
            return "bytes"
        elif field_type.is_a(IdlType.STRING):
            return "str"
        elif field_type.is_a(IdlType.PUBLIC_KEY):
            editor.add_from_import("solana.publickey", "PublicKey")
            return "PublicKey"
        elif field_type.is_a(IdlType.DEFINED):
            if field_type.field not in self._all_defined_types:
                if field_type.field in self.external_types:
                    return self.external_types[field_type.field](editor)

            self._expected_types.add(field_type.field)
            if within_types:
                editor.add_from_import(
                    f"{self.root_module}.types.{pascal_to_snake(field_type.field)}",
                    field_type.field,
                )
                if explicit_forward_ref or field_type.field in self._defined_types:
                    return f"{field_type.field}"
                else:
                    return f'"{field_type.field}"'
            else:
                editor.add_from_import(f"{self.root_module}.types", field_type.field)
                return f"{field_type.field}"
        elif int(field_type) in (
            int(IdlType.OPTION),
            int(IdlType.COPTION),
            int(IdlType.STATIC),
            int(IdlType.VEC),
        ):
            if field_type.is_a(IdlType.COPTION):
                type_name = "COption"
                editor.add_from_import(f"solmate.dtypes", type_name)
            else:
                if field_type.is_a(IdlType.OPTION):
                    type_name = "Option"
                elif field_type.is_a(IdlType.STATIC):
                    type_name = "Static"
                else:
                    type_name = "Vec"

                editor.add_from_import(f"pod", type_name)

            field_type_str = self._get_type_as_string(
                field_type.field, editor, within_types=within_types
            )
            return f"{type_name}[{field_type_str}]"

        elif field_type.is_a(IdlType.ARRAY):
            editor.add_from_import("pod", "FixedLenArray")
            elem_type, n_elem = field_type.field
            elem_type_str = self._get_type_as_string(
                elem_type, editor, within_types=within_types
            )
            return f"FixedLenArray[{elem_type_str}, {n_elem}]"

        return ""

    def _get_type_definitions(self) -> Iterable[IdlTypeDefinition]:
        return self.idl.types + self.idl.accounts

    def _generate_types(self):
        type_definitions = self._get_type_definitions()
        if not type_definitions:
            return

        module_editor = self._get_editor(f"{self.root_module}.types", is_file=False)
        for type_def in type_definitions:
            editor = self._get_editor(
                f"{self.root_module}.types.{camel_to_snake(type_def.name)}"
            )
            editor.add_from_import("pod", "pod")

            class_code = ["@pod\n"]
            if type_def.type.is_a(IdlTypeDefinitionTy.STRUCT):
                class_code += [f"class {type_def.name}:\n"]
                has_field = False
                for field in type_def.type.field.fields:
                    field_name = camel_to_snake(field.name)
                    field_type = self._get_type_as_string(
                        field.type, editor, within_types=True
                    )
                    class_code.append(f"    {field_name}: {field_type}\n")
                    has_field = True

                if not has_field:
                    class_code += ["    pass\n"]

            else:
                editor.add_from_import("pod", "Enum")
                editor.add_from_import("pod", "AutoTagType")
                class_code += [f"class {type_def.name}(Enum[AutoTagType]):\n"]
                variants = type_def.type.field.variants
                for variant in variants:
                    if variant.fields is None:
                        variant_type = "None"
                    elif variant.fields.is_a(EnumFields.NAMED):
                        editor.add_from_import("pod", "Variant")
                        editor.add_from_import("pod", "named_fields")
                        # TODO complete me
                        named_fields = variant.fields.field
                        raise NotImplementedError()
                    else:
                        editor.add_from_import("pod", "Variant")

                        tuple_fields = []
                        for field_type in variant.fields.field:
                            tuple_fields.append(
                                self._get_type_as_string(
                                    field_type,
                                    editor,
                                    within_types=True,
                                    explicit_forward_ref=True,
                                )
                            )

                        if len(tuple_fields) == 0:
                            variant_type = "None"
                        elif len(tuple_fields) == 1:
                            variant_type = "Variant(field=" + tuple_fields[0] + ")"
                        else:
                            editor.add_from_import("typing", "Tuple")
                            variant_type = (
                                "Variant(field=Tuple[" + ", ".join(tuple_fields) + "])"
                            )

                    variant_name = pascal_to_snake(variant.name).upper()
                    class_code += [f"    {variant_name} = {variant_type}\n"]

                if not variants:
                    class_code += ["    pass\n"]

            if editor.set_with_lock(f"class({type_def.name})", class_code):
                self._add_packing_methods(
                    editor, type_def.type.is_a(IdlTypeDefinitionTy.STRUCT)
                )

            module_editor.add_from_import(
                f".{camel_to_snake(type_def.name)}", type_def.name
            )

            self._defined_types.add(type_def.name)
            self._package_editor.add_import(f"{self.root_module}.types", "types")

    def _generate_constants(self):
        if not self.idl.constants:
            return

        editor = self._get_editor(f"{self.root_module}.constants")
        code = []

        for const in self.idl.constants:
            const_type = self._get_type_as_string(
                const.type, editor, within_types=False
            )
            code.append(f"{const.name}: {const_type} = {const.value}\n")

        editor.set_with_lock("constants", code)
        self._package_editor.add_import(f"{self.root_module}.constants", "constants")

    def _generate_accounts(self):
        if not self.idl.accounts or self.accnt_tag_values is None:
            return

        editor = self._get_editor(f"{self.root_module}.accounts")
        code = []

        editor.add_from_import("pod", "pod")
        editor.add_from_import("pod", "Enum")

        base = None
        variant_type = None
        if self.accnt_tag_values == "incremental":
            editor.add_from_import("pod", "Variant")
            base = "Enum"
            variant_type = "Variant"

        elif self.accnt_tag_values == "anchor":
            editor.add_from_import("pod", "U64")
            editor.add_from_import("solmate.anchor", "AccountDiscriminant")
            base = "Enum[U64]"
            variant_type = "AccountDiscriminant"

        code.extend(
            [
                "@pod\n",
                f"class Accounts({base}):\n",
            ]
        )
        for account in self.idl.accounts:
            editor.add_from_import(
                f"{self.root_module}.types.{pascal_to_snake(account.name)}",
                account.name,
            )

            variant_name = pascal_to_snake(account.name).upper()
            variant_inst = f"{variant_type}(field={account.name})"
            code += [f"    {variant_name} = {variant_inst}\n"]

        if editor.set_with_lock("accounts", code):
            self._add_packing_methods(editor, is_struct=True)

        self._package_editor.add_import(f"{self.root_module}.accounts", "accounts")

    @staticmethod
    def _flatten_accounts(accounts: Vec[IdlAccountItem]):
        flat = []
        for account in accounts:
            if int(account) == int(IdlAccountItem.IDL_ACCOUNT):
                flat.append(account)
            else:
                flat += CodeGen._flatten_accounts(account.field)

        return flat

    def _generate_instruction(self, module_editor: CodeEditor, instr: IdlInstruction):
        instr_name = camel_to_snake(instr.name)
        instr_accounts = self._flatten_accounts(instr.accounts)

        editor = self._get_editor(f"{self.root_module}.instructions.{instr_name}")
        editor.add_from_import("solana.transaction", "AccountMeta")
        editor.add_from_import("solana.publickey", "PublicKey")
        editor.add_from_import("dataclasses", "dataclass")
        editor.add_from_import("typing", "Optional")
        editor.add_from_import("typing", "List")

        # generating instruction account metas
        module_editor.add_from_import(
            f".{instr_name}", f"{snake_to_pascal(instr_name)}Ix"
        )
        module_editor.add_from_import(f".{instr_name}", f"{instr_name}")
        code = [
            "@dataclass\n" f"class {snake_to_pascal(instr_name)}Ix:\n",
            "    program_id: PublicKey\n",
            "\n",
            "    # account metas\n",
        ]
        for account in instr_accounts:
            account_name = camel_to_snake(account.field.name)
            account_type = (
                "Optional[AccountMeta]" if account.field.is_optional else "AccountMeta"
            )
            code.append(f"    {account_name}: {account_type}\n")

        code.append(f"    remaining_accounts: Optional[List[AccountMeta]]\n")

        # generating instruction data fields
        if len(instr.args) > 0:
            code += [
                "\n",
                "    # data fields\n",
            ]
        for arg in instr.args:
            arg_type = self._get_type_as_string(arg.type, editor, within_types=False)
            code.append(f"    {arg.name}: {arg_type}\n")

        # generating to_instruction() function
        code.append("\n")
        code.append("    def to_instruction(self):\n")
        code.append("        keys = []\n")
        for account in instr_accounts:
            account_name = camel_to_snake(account.field.name)
            if account.field.is_optional:
                code.append(f"        if self.{account_name} is not None:\n")
                code.append(f"            keys.append(self.{account_name})\n")
            else:
                code.append(f"        keys.append(self.{account_name})\n")

        code.append(f"        if self.remaining_accounts is not None:\n")
        code.append(f"            keys.extend(self.remaining_accounts)\n")
        code.append("\n")

        # generating data
        editor.add_from_import("io", "BytesIO")
        code.append("        buffer = BytesIO()\n")
        editor.add_from_import(".instruction_tag", "InstructionTag")
        instr_tag_name = camel_to_snake(instr.name).upper()
        code.append(
            f"        buffer.write(InstructionTag.to_bytes(InstructionTag.{instr_tag_name}))\n"
        )
        for arg in instr.args:
            arg_type = self._get_type_as_string(arg.type, editor, within_types=False)
            code.append(f"        buffer.write({arg_type}.to_bytes(self.{arg.name}))\n")
        code.append("\n")

        editor.add_from_import("solana.transaction", "TransactionInstruction")
        code.append("        return TransactionInstruction(\n")
        code.append("            keys=keys,\n")
        code.append(f"            program_id=self.program_id,\n")
        code.append("            data=buffer.getvalue(),\n")
        code.append("        )\n")
        code.append("\n")
        if editor.set_with_lock(f"ix_cls({instr_name})", code):
            editor.add_lines("\n", "\n")

        # generating helper function's code
        code = [f"def {instr_name}(\n"]

        # arguments
        args_without_default = []
        args_with_default = []
        editor.add_from_import("typing", "Union")
        meta_type = "Union[str, PublicKey, AccountMeta]"
        for account in instr_accounts:
            account_name = camel_to_snake(account.field.name)
            account_type = (
                f"Optional[{meta_type}]" if account.field.is_optional else meta_type
            )
            default_account = self.default_accounts.get(account_name, None)
            if default_account is not None:
                args_with_default.append(
                    (account_name, account_type, f'PublicKey("{default_account}")')
                )
            elif account.field.is_optional:
                args_with_default.append((account_name, account_type, "None"))
            else:
                args_without_default.append((account_name, account_type))

        for arg in instr.args:
            arg_type = self._get_type_as_string(arg.type, editor, within_types=False)
            args_without_default.append((arg.name, arg_type))

        args_with_default.append(
            ("remaining_accounts", "Optional[List[AccountMeta]]", "None")
        )
        editor.add_import(self.root_module)
        args_with_default.append(("program_id", "Optional[PublicKey]", "None"))

        for arg_name, arg_type in args_without_default:
            code.append(f"    {arg_name}: {arg_type},\n")

        for arg_name, arg_type, arg_val in args_with_default:
            code.append(f"    {arg_name}: {arg_type} = {arg_val},\n")

        code.append(f"):\n")

        # helper's body
        code.append("    if program_id is None:\n")
        code.append(f"        program_id = {self.root_module}.PROGRAM_ID\n")
        code.append("\n")

        editor.add_from_import("solmate.utils", "to_account_meta")
        for account in instr_accounts:
            account_name = camel_to_snake(account.field.name)
            code.append(f"    if isinstance({account_name}, (str, PublicKey)):\n")
            code.append(f"        {account_name} = to_account_meta(\n")
            code.append(f"            {account_name},\n")
            code.append(f"            is_signer={account.field.is_signer},\n")
            code.append(f"            is_writable={account.field.is_mut},\n")
            code.append(f"        )\n")
        code.append("\n")

        # creating the instruction and returning it as a regular instruction
        code.append(f"    return {snake_to_pascal(instr_name)}Ix(\n")
        code.append(f"        program_id=program_id,\n")
        for account in instr_accounts:
            account_name = camel_to_snake(account.field.name)
            code.append(f"        {account_name}={account_name},\n")
        code.append(f"        remaining_accounts=remaining_accounts,\n")
        for arg in instr.args:
            code.append(f"        {arg.name}={arg.name},\n")
        code.append(f"    ).to_instruction()\n")
        code.append(f"\n")

        # writing instruction class
        editor.set_with_lock(f"ix_fn({instr_name})", code)

    def _generate_instructions(self):
        if not self.idl.instructions:
            return

        module_editor = self._get_editor(
            f"{self.root_module}.instructions", is_file=False
        )
        for instr in self.idl.instructions:
            self._generate_instruction(module_editor, instr)

        # generating InstructionTag class
        instr_tag_editor = self._get_editor(
            f"{self.root_module}.instructions.instruction_tag"
        )
        instr_tag_editor.add_from_import("pod", "Enum")
        if self.instr_tag_values == "incremental":
            tag_type = "U8"
            variant_type = "Variant"
            instr_tag_editor.add_from_import("pod", "Variant")
        else:
            tag_type = "U64"
            variant_type = "InstructionDiscriminant"
            instr_tag_editor.add_from_import("solmate.anchor", "InstructionDiscriminant")

        instr_tag_editor.add_from_import("pod", "pod")
        instr_tag_editor.add_from_import("pod", tag_type)
        instr_tag_code = [
            "@pod\n",
            f"class InstructionTag(Enum[{tag_type}]):\n",
        ]
        for instr in self.idl.instructions:
            instr_tag_name = camel_to_snake(instr.name).upper()
            instr_tag_code.append(f"    {instr_tag_name} = {variant_type}()\n")

        instr_tag_editor.set_with_lock(f"instruction_tag", instr_tag_code)
        module_editor.add_from_import(".instruction_tag", "InstructionTag")

        self._package_editor.add_import(
            f"{self.root_module}.instructions", "instructions"
        )

    def _generate_events(self):
        if not self.idl.events:
            return

        # TODO implement code generation for events
        print("Skipping events...")

    def _generate_errors(self):
        if not self.idl.errors:
            return

        # TODO implement code generation for errors
        print("Skipping errors...")

    def _generate_state(self):
        if not self.idl.state:
            return

        # TODO implement code generation for state
        print("Skipping state...")

    def generate_code(self, check_missing_types=False):
        self._package_editor = self._get_editor(self.root_module, is_file=False)

        self._package_editor.add_from_import("solana.publickey", "PublicKey")
        self._package_editor.set_with_lock(
            "program_id", [f'PROGRAM_ID = PublicKey("{self.program_id}")\n']
        )

        self._generate_types()
        self._generate_constants()
        self._generate_accounts()
        self._generate_instructions()
        self._generate_events()
        self._generate_errors()
        self._generate_state()

        undefined_types = self._expected_types.difference(self._defined_types)
        if undefined_types:
            if check_missing_types:
                raise RuntimeError(
                    f"The following types are used but not defined: {undefined_types}"
                )
            else:
                print(
                    f"The following types are used but not defined: {undefined_types}"
                )

    def save_modules(self):
        for editor in self._editors.values():
            editor.save()


def usize_type(editor: CodeEditor):
    editor.add_from_import("solmate.dtypes", "Usize")
    return "Usize"


def unix_timestamp_type(
    editor: CodeEditor,
):
    editor.add_from_import("solmate.dtypes", "UnixTimestamp")
    return "UnixTimestamp"


def program_error_type(editor: CodeEditor):
    editor.add_from_import("solmate.dtypes", "ProgramError")
    return "ProgramError"


def self_trade_behavior_type(editor: CodeEditor):
    editor.add_from_import("dexterity.utils.aob.state.base", "SelfTradeBehavior")
    return "SelfTradeBehavior"


def side_type(editor: CodeEditor):
    editor.add_from_import("dexterity.utils.aob.state.base", "Side")
    return "Side"


def defined_types_to_imports(
    root_module: str, idl: Idl
) -> Dict[str, Callable[[CodeEditor], str]]:
    def add_import(name: str, editor: CodeEditor) -> str:
        editor.add_from_import(f"{root_module}.types.{pascal_to_snake(name)}", name)
        return name

    type_definitions = idl.types + idl.accounts
    return dict(((ty.name, partial(add_import, ty.name)) for ty in type_definitions))


def cli(
    idl_dir: str,
    out_dir: str,
    pids_dir: Union[str, Dict[str, PublicKey]],
    parent_module: str,
    skip_types: Set[str],
):
    protocol_to_idl_and_types = {}
    protocol_to_pid = get_protocols(idl_dir, pids_dir)
    for protocol in protocol_to_pid.keys():
        idl = Idl.from_json_file(f"{idl_dir}/{protocol}.json")

        idl.types = list(filter(lambda x: x.name not in skip_types, idl.types))
        idl.accounts = list(filter(lambda x: x.name not in skip_types, idl.accounts))
        protocol_to_idl_and_types[protocol] = (
            idl,
            defined_types_to_imports(f"{parent_module}.{protocol}", idl),
        )

    external_types = {
        "usize": usize_type,
        "UnixTimestamp": unix_timestamp_type,
        "ProgramError": program_error_type,
        "SelfTradeBehavior": self_trade_behavior_type,
        "Side": side_type,
    }
    # allow each IDL to reference types defined in other IDLs
    for (_, exported_types) in protocol_to_idl_and_types.values():
        external_types.update(exported_types)

    for protocol, (idl, _) in protocol_to_idl_and_types.items():
        print(f"Generating code for {protocol}")
        codegen = CodeGen(
            idl,
            protocol_to_pid[protocol],
            f"{parent_module}.{protocol}",
            out_dir,
            external_types=external_types,
            default_accounts={
                "systemProgram": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
                "sysvar_rent": SYSVAR_RENT_PUBKEY,
            },
            accnt_tag_values="anchor",
            instr_tag_values="anchor",
        )
        codegen.generate_code(check_missing_types=not True)
        codegen.save_modules()


def get_protocols(idl_dir: str, pids: Union[str, Dict[str, str]]) -> Dict[str, str]:
    protocols = set()
    for filename in os.listdir(idl_dir):
        match = re.search(r"([a-z_\-]+).json", filename)
        if match is None:
            continue
        protocol = match.groups()[0]
        protocols.add(protocol)

    # if a path was passed in, load pids from the directory
    if isinstance(pids, str):
        pids = dir_to_pids(pids)

    intersection = {}
    for protocol, pid in pids.items():
        if protocol in protocols:
            intersection[protocol] = pid
    for protocol in protocols:
        if protocol not in pids:
            print("WARNING: found idl file with no matching program id: ", protocol)

    return intersection


def dir_to_pids(dir: str) -> Dict[str, str]:
    program_to_id = {}
    for filename in os.listdir(dir):
        match = re.search(r"([a-z_]+)-keypair.json", filename)
        if match is None:
            continue
        program = match.groups()[0]
        program_to_id[program] = run(f"solana-keygen pubkey {dir}/{filename}")
    return program_to_id


def run(cmd, debug=False):
    if debug:
        print(cmd)
    res = subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
    if debug:
        print(res)
    return res
