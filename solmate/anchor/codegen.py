import os
from typing import Dict, Iterable, Set, Union, Callable, Literal, Optional

from podite import Vec
from solana.publickey import PublicKey

from solmate.utils import camel_to_snake, pascal_to_snake, snake_to_pascal
from .editor import CodeEditor
from .idl import (
    Idl,
    IdlTypeDefinition,
    IdlTypeDefinitionTy,
    IdlType,
    EnumFields,
    IdlAccountItem,
    IdlInstruction,
    IdlAccount,
)


def add_packing_methods(editor, is_struct):
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


class InstructionCodeGen:
    codegen: "CodeGen"
    editor: "CodeEditor"
    module_editor: "CodeEditor"
    instr: IdlInstruction
    instr_account: list[tuple[IdlAccount, str]]
    flattening_mode: Literal["ignore", "prefix"]

    def __init__(
        self,
        codegen: "CodeGen",
        module_editor: CodeEditor,
        instr: IdlInstruction,
        flattening_mode: Literal["ignore", "prefix"] = "ignore",
    ):
        self.codegen = codegen
        self.module_editor = module_editor
        self.instr = instr
        self.flattening_mode = flattening_mode
        self.instr_accounts = self.get_instr_accounts()

    @property
    def instr_name(self):
        return camel_to_snake(self.instr.name)

    def _flatten_accounts(self, accounts: Vec[IdlAccountItem], name_prefix=""):
        flat = []
        for account in accounts:
            if int(account) == int(IdlAccountItem.IDL_ACCOUNT):
                if self.flattening_mode == "ignore":
                    name = account.field.name
                elif self.flattening_mode == "prefix":
                    name = name_prefix + account.field.name
                else:
                    raise ValueError()
                flat.append((account.field, camel_to_snake(name)))
            else:
                prefix = f"{name_prefix}{account.field.name}_"
                flat += InstructionCodeGen._flatten_accounts(
                    account.field.accounts, prefix
                )

        return flat

    def get_instr_accounts(self):
        accounts = self._flatten_accounts(self.instr.accounts)
        accounts.append(
            (
                IdlAccount(
                    name="remaining_accounts",
                    is_mut=False,
                    is_signer=False,
                    is_optional=True,
                    is_array=True,
                ),
                "remaining_accounts",
            )
        )

        return accounts

    def get_default_account(self, editor, account, account_name):
        default_account = self.codegen.default_accounts.get(account_name, None)
        if default_account is not None:
            if isinstance(default_account, (str, PublicKey)):
                if default_account == "None":
                    expr = "None"
                else:
                    expr = f'PublicKey("{default_account}")'
            else:
                expr = default_account(editor)
            return expr
        return None

    def get_default_value(self, editor, arg):
        return None

    def generate_ix_cls_declaration(self):
        instr_name = self.instr_name
        self.module_editor.add_from_import(
            f".{instr_name}", f"{snake_to_pascal(instr_name)}Ix"
        )
        self.editor.add_from_import("dataclasses", "dataclass")

        return [
            "@dataclass\n",
            f"class {snake_to_pascal(instr_name)}Ix:\n",
        ]

    def generate_ix_cls_metas_fields(self):
        editor = self.editor

        editor.add_from_import("solana.transaction", "AccountMeta")
        editor.add_from_import("solana.publickey", "PublicKey")
        editor.add_from_import("typing", "Optional")
        editor.add_from_import("typing", "List")

        code = [
            "    program_id: PublicKey\n",
            "\n",
            "    # account metas\n",
        ]
        for account, account_name in self.instr_accounts:
            inner_type = "List[AccountMeta]" if account.is_array else "AccountMeta"
            account_type = (
                f"Optional[{inner_type}]" if account.is_optional else inner_type
            )
            code.append(f"    {account_name}: {account_type}\n")

        return code

    def generate_ix_cls_args_fields(self):
        editor = self.editor
        instr = self.instr

        code = []
        if len(instr.args) > 0:
            code += [
                "\n",
                "    # data fields\n",
            ]
        for arg in instr.args:
            arg_type = self.codegen.get_type_as_string(
                arg.type, editor, within_types=False
            )
            code.append(f"    {arg.py_name}: {arg_type}\n")

        return code

    def generate_ix_cls_to_instruction_method(self):
        editor = self.editor
        instr = self.instr

        code = [
            "\n",
            "    def to_instruction(self):\n",
            "        keys = []\n",
        ]
        for account, account_name in self.instr_accounts:
            if account.is_optional:
                code.append(f"        if self.{account_name} is not None:\n")
                nest = 3
            else:
                nest = 2

            indent = "    " * nest

            if account.is_array:
                code.append(indent + f"keys.extend(self.{account_name})\n")
            else:
                code.append(indent + f"keys.append(self.{account_name})\n")

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
            arg_type = self.codegen.get_type_as_string(
                arg.type, editor, within_types=False
            )

            editor.add_from_import("podite", "BYTES_CATALOG")
            code.append(
                f"        buffer.write(BYTES_CATALOG.pack({arg_type}, self.{arg.py_name}))\n"
            )
        code.append("\n")

        editor.add_from_import("solana.transaction", "TransactionInstruction")
        code.append("        return TransactionInstruction(\n")
        code.append("            keys=keys,\n")
        code.append(f"            program_id=self.program_id,\n")
        code.append("            data=buffer.getvalue(),\n")
        code.append("        )\n")
        code.append("\n")
        return code

    def generate_ix_cls(self):
        code = self.generate_ix_cls_declaration()
        code += self.generate_ix_cls_metas_fields()
        code += self.generate_ix_cls_args_fields()
        code += self.generate_ix_cls_to_instruction_method()

        return code

    def generate_ix_func_declaration(self):
        instr_name = self.instr_name
        self.module_editor.add_from_import(f".{instr_name}", f"{instr_name}")

        # generating helper function's code
        code = [f"def {instr_name}(\n"]
        code += self.generate_ix_func_args()
        code += ["):\n"]
        return code

    def generate_ix_func_args(self):
        code = []
        editor = self.editor
        codegen = self.codegen
        instr = self.instr

        editor.add_from_import("solana.transaction", "AccountMeta")
        editor.add_from_import("solana.publickey", "PublicKey")
        editor.add_from_import("typing", "Optional")
        editor.add_from_import("typing", "List")

        args_without_default = []
        args_with_default = []
        editor.add_from_import("typing", "Union")
        meta_type = "Union[str, PublicKey, AccountMeta]"
        for account, account_name in self.instr_accounts:
            default_account = self.get_default_account(editor, account, account_name)

            if account.is_array:
                inner_type = f"List[{meta_type}]"
            else:
                inner_type = meta_type

            if account.is_optional or default_account == "None":
                account_type = f"Optional[{inner_type}]"
            else:
                account_type = inner_type

            if default_account is not None:
                args_with_default.append((account_name, account_type, default_account))
            elif account.is_optional:
                args_with_default.append((account_name, account_type, "None"))
            else:
                args_without_default.append((account_name, account_type))

        for arg in instr.args:
            arg_type = codegen.get_type_as_string(arg.type, editor, within_types=False)
            arg_value = self.get_default_value(editor, arg)
            if arg_value is None:
                args_without_default.append((arg.py_name, arg_type))
            else:
                args_with_default.append((arg.py_name, arg_type, arg_value))

        program_id = self.get_default_account(editor, None, "program_id")
        if program_id is None:
            args_without_default.append(("program_id", "PublicKey"))
        else:
            args_with_default.append(("program_id", "PublicKey", program_id))

        for arg_name, arg_type in args_without_default:
            code.append(f"    {arg_name}: {arg_type},\n")

        for arg_name, arg_type, arg_val in args_with_default:
            code.append(f"    {arg_name}: {arg_type} = {arg_val},\n")

        return code

    def generate_ix_func_key_preprocessor(self, account, account_name):
        self.editor.add_from_import("solmate.utils", "to_account_meta")

        if account.is_array:
            if account.is_optional:
                return [
                    f"    if isinstance({account_name}, list):\n",
                    f"        for i in range(len({account_name})):\n",
                    f"            if isinstance({account_name}[i], (str, PublicKey)):\n",
                    f"                {account_name}[i] = to_account_meta(\n",
                    f"                    {account_name}[i],\n",
                    f"                    is_signer={account.is_signer},\n",
                    f"                    is_writable={account.is_mut},\n",
                    f"                )\n",
                ]
            else:
                return [
                    f"    for i in range(len({account_name})):\n",
                    f"        if isinstance({account_name}[i], (str, PublicKey)):\n",
                    f"            {account_name}[i] = to_account_meta(\n",
                    f"                {account_name}[i],\n",
                    f"                is_signer={account.is_signer},\n",
                    f"                is_writable={account.is_mut},\n",
                    f"            )\n",
                ]

        else:
            return [
                f"    if isinstance({account_name}, (str, PublicKey)):\n",
                f"        {account_name} = to_account_meta(\n",
                f"            {account_name},\n",
                f"            is_signer={account.is_signer},\n",
                f"            is_writable={account.is_mut},\n",
                f"        )\n",
            ]

    def generate_ix_func_keys_compiler(self):
        code = []
        for account, prefix in self.instr_accounts:
            code += self.generate_ix_func_key_preprocessor(account, prefix)
            code.append("\n")
        return code

    def generate_ix_func_return_obj(self):
        # creating the instruction and returning it as a regular instruction
        instr = self.instr
        instr_name = self.instr_name
        instr_accounts = self.instr_accounts

        code = [
            f"    return {snake_to_pascal(instr_name)}Ix(\n",
            f"        program_id=program_id,\n",
        ]
        for account, account_name in instr_accounts:
            code.append(f"        {account_name}={account_name},\n")
        for arg in instr.args:
            code.append(f"        {arg.py_name}={arg.py_name},\n")
        code.append(f"    ).to_instruction()\n")
        code.append(f"\n")
        return code

    def generate_ix_func(self):
        code = self.generate_ix_func_declaration()
        code += self.generate_ix_func_keys_compiler()
        code += self.generate_ix_func_return_obj()

        return code

    def generate(self):
        """
        Generates python files for constructing and serializing each instruction in the idl
        """
        self.editor = self.codegen.get_editor(
            f"{self.codegen.root_module}.instructions.{self.instr_name}"
        )

        ix_cls = self.generate_ix_cls()
        if self.editor.set_with_lock(f"ix_cls({self.instr_name})", ix_cls):
            self.editor.add_lines("\n", "\n")

        ix_func = self.generate_ix_func()
        self.editor.set_with_lock(f"ix_fn({self.instr_name})", ix_func)


class AccountsCodeGen:
    codegen: "CodeGen"
    editor: "CodeEditor"
    module_editor: "CodeEditor"
    package_editor: "CodeEditor"
    accounts: Vec[IdlTypeDefinition]

    def __init__(
        self,
        codegen: "CodeGen",
        package_editor: CodeEditor,
        accounts: Vec[IdlTypeDefinition],
    ):
        self.codegen = codegen
        self.module_editor = codegen.get_editor(f"{codegen.root_module}.accounts")
        self.package_editor = package_editor
        self.accounts = accounts

    def generate_accounts_cls_declaration(self):
        editor = self.module_editor

        editor.add_from_import("podite", "pod")
        editor.add_from_import("podite", "Enum")

        base = None

        if self.codegen.accnt_tag_values == "anchor":
            editor.add_from_import("podite", "U64")
            editor.add_from_import("solmate.anchor", "AccountDiscriminant")
            base = "Enum[U64]"

        elif self.codegen.accnt_tag_values is not None:
            tag_type = self.codegen.accnt_tag_values.split(":")[1]
            editor.add_from_import("podite", "Variant")
            editor.add_from_import("podite", tag_type)
            base = f"Enum[{tag_type}]"

        return [
            "@pod\n",
            f"class Accounts({base}):\n",
        ]

    def generate_accounts_cls_variants(self):
        editor = self.module_editor

        editor.add_from_import("podite", "pod")
        editor.add_from_import("podite", "Enum")

        variant_type = None

        if self.codegen.accnt_tag_values == "anchor":
            editor.add_from_import("podite", "U64")
            editor.add_from_import("solmate.anchor", "AccountDiscriminant")
            variant_type = "AccountDiscriminant"

        elif self.codegen.accnt_tag_values is not None:
            tag_type = self.codegen.accnt_tag_values.split(":")[1]
            editor.add_from_import("podite", "Variant")
            editor.add_from_import("podite", tag_type)
            variant_type = "Variant"

        code = []
        for account in self.accounts:
            editor.add_from_import(
                f"{self.codegen.root_module}.types.{pascal_to_snake(account.name)}",
                account.name,
            )

            variant_name = pascal_to_snake(account.name).upper()
            variant_inst = f"{variant_type}(field={account.name})"
            code += [f"    {variant_name} = {variant_inst}\n"]

        return code

    def generate_accounts_cls_packing_logic(self):
        return []

    def generate_accounts_cls_packing_methods(self):
        add_packing_methods(self.module_editor, is_struct=True)

    def generate_accounts_cls(self):
        code = self.generate_accounts_cls_declaration()
        code += self.generate_accounts_cls_variants()
        code += self.generate_accounts_cls_packing_logic()

        if self.module_editor.set_with_lock("accounts", code):
            self.generate_accounts_cls_packing_methods()

    def generate(self):
        codegen = self.codegen

        if not codegen.idl.accounts or codegen.accnt_tag_values is None:
            return

        self.generate_accounts_cls()
        self.package_editor.add_import(
            f"{self.codegen.root_module}.accounts", "accounts"
        )


class CodeGen:
    """
    Codegen is instantiated for each idl file and generates a client based off that idl.

    To customize client generation, subclass Codegen and override one of the generation functions

    :param idl: The parsed idl file
    :param addresses: Dict from address name to PublicKey for hardcoded associated account addresses
    :param root_module: Name of the root module. If periods are included (e.g. "outer.mid.inner"), multiple directories
                         are created
    :param source_path: Path where the root_module will be output
    :param external_types: Dict from idl typename to function that manages importing the type and returning
                            the in-code typename
    :param default_accounts: Dict from account name to default PublicKey used to populate function
                              argument defaults for convenience
    :param instr_tag_values: Determines how large the instruction tag should be. For anchor programs use "anchor" or omit the arg
    :param accnt_tag_values: Determines how large the account tag should be. For anchor programs use "anchor" or omit the arg
    """

    idl: Idl
    addresses: Dict[str, str]
    root_module: str
    source_path: str
    external_types: Dict[str, Callable]
    default_accounts: Dict[str, Union[PublicKey, str, Callable]]
    instr_tag_values: Literal[
        "anchor",
        "incremental:U8",
        "incremental:U16",
        "incremental:U32",
        "incremental:U64",
        "incremental:U128",
    ]
    accnt_tag_values: Optional[
        Literal[
            "anchor",
            "incremental:U8",
            "incremental:U16",
            "incremental:U32",
            "incremental:U64",
            "incremental:U128",
        ]
    ]

    _editors: Dict[str, CodeEditor]
    _all_defined_types: Set[str]  # all type names for this module
    _defined_types: Set[str]  # all type names for which code is generated
    _expected_types: Set[str]  # all type names used somewhere in this module
    _package_editor: CodeEditor

    def __init__(
        self,
        idl,
        addresses,
        root_module,
        source_path,
        external_types: Dict[str, Callable[[CodeEditor], str]] = None,
        default_accounts=None,
        instr_tag_values="incremental[U8]",
        accnt_tag_values="incremental[U8]",
        skip_types=None,
    ):
        self.idl = idl
        self.addresses = addresses
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
        for type_def in self.get_type_definitions():
            self._all_defined_types.add(type_def.name)

    def get_editor(self, name, is_file=True) -> CodeEditor:
        if name not in self._editors:
            subpath = name.replace(".", "/")
            if not is_file:
                subpath += "/__init__"
            subpath += ".py"

            fullpath = os.path.join(self.source_path, subpath)
            self._editors[name] = CodeEditor(fullpath)
            self._editors[name].load()

        return self._editors[name]

    def get_type_as_string(
        self, field_type, editor, within_types, explicit_forward_ref=False
    ):
        """
        Convert the idl type to the python type as well as add the required imports
        """
        if field_type.is_a(IdlType.BOOL):
            return "bool"
        elif field_type <= IdlType.I128:
            editor.add_from_import("podite", field_type.get_name())
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

                editor.add_from_import(f"podite", type_name)

            field_type_str = self.get_type_as_string(
                field_type.field, editor, within_types=within_types
            )
            return f"{type_name}[{field_type_str}]"

        elif field_type.is_a(IdlType.ARRAY):
            editor.add_from_import("podite", "FixedLenArray")
            elem_type, n_elem = field_type.field
            elem_type_str = self.get_type_as_string(
                elem_type, editor, within_types=within_types
            )
            return f"FixedLenArray[{elem_type_str}, {n_elem}]"

        return ""

    def get_type_definitions(self) -> Iterable[IdlTypeDefinition]:
        return self.idl.types + self.idl.accounts

    def generate_types(self):
        """
        Method that generates python files for each type defined in the idl
        """
        type_definitions = self.get_type_definitions()
        if not type_definitions:
            return

        module_editor = self.get_editor(f"{self.root_module}.types", is_file=False)
        for type_def in type_definitions:
            editor = self.get_editor(
                f"{self.root_module}.types.{camel_to_snake(type_def.name)}"
            )
            editor.add_from_import("podite", "pod")

            class_code = ["@pod\n"]
            if type_def.type.is_a(IdlTypeDefinitionTy.STRUCT):
                class_code += [f"class {type_def.name}:\n"]
                has_field = False
                for field in type_def.type.field.fields:
                    field_name = camel_to_snake(field.name)
                    field_type = self.get_type_as_string(
                        field.type, editor, within_types=True
                    )
                    class_code.append(f"    {field_name}: {field_type}\n")
                    has_field = True

                if not has_field:
                    class_code += ["    pass\n"]

            else:
                editor.add_from_import("podite", "Enum")
                editor.add_from_import("podite", "AutoTagType")
                class_code += [f"class {type_def.name}(Enum[AutoTagType]):\n"]
                variants = type_def.type.field.variants
                for variant in variants:
                    if variant.fields is None:
                        variant_type = "None"
                    elif variant.fields.is_a(EnumFields.NAMED):
                        editor.add_from_import("podite", "Variant")
                        editor.add_from_import("podite", "named_fields")
                        editor.add_from_import("podite", "Option")

                        named_fields = []
                        for field in variant.fields.field:
                            field_name = field.name
                            field_type = self.get_type_as_string(
                                field.type,
                                editor,
                                within_types=True,
                                explicit_forward_ref=True,
                            )
                            named_fields.append(f"{field_name}={field_type}")

                        if len(named_fields) == 0:
                            variant_type = "None"
                        else:
                            variant_type = (
                                "Variant(field=named_fields("
                                + ", ".join(named_fields)
                                + "))"
                            )
                    else:
                        editor.add_from_import("podite", "Variant")

                        tuple_fields = []
                        for field_type in variant.fields.field:
                            tuple_fields.append(
                                self.get_type_as_string(
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
                add_packing_methods(
                    editor, type_def.type.is_a(IdlTypeDefinitionTy.STRUCT)
                )

            module_editor.add_from_import(
                f".{camel_to_snake(type_def.name)}", type_def.name
            )

            self._defined_types.add(type_def.name)
            self._package_editor.add_import(f"{self.root_module}.types", "types")

    def generate_addresses(self):
        editor = self.get_editor(f"{self.root_module}.addrs")

        editor.add_from_import("solana.publickey", "PublicKey")

        code = []
        for name, addr in self.addresses.items():
            code.append(f'{name} = PublicKey("{addr}")\n')
            self._package_editor.add_from_import(f"{self.root_module}.addrs", name)
        editor.set_with_lock("addresses", code)

    def generate_constants(self):
        if not self.idl.constants:
            return

        editor = self.get_editor(f"{self.root_module}.constants")
        code = []

        for const in self.idl.constants:
            const_type = self.get_type_as_string(const.type, editor, within_types=False)
            code.append(f"{const.name}: {const_type} = {const.value}\n")

        editor.set_with_lock("constants", code)
        self._package_editor.add_import(f"{self.root_module}.constants", "constants")

    def generate_accounts(self):
        return AccountsCodeGen(self, self._package_editor, self.idl.accounts).generate()

    def generate_instruction(self, module_editor, instr):
        return InstructionCodeGen(self, module_editor, instr).generate()

    def generate_instructions(self):
        if not self.idl.instructions:
            return

        module_editor = self.get_editor(
            f"{self.root_module}.instructions", is_file=False
        )
        for instr in self.idl.instructions:
            self.generate_instruction(module_editor, instr)

        # generating InstructionTag class
        instr_tag_editor = self.get_editor(
            f"{self.root_module}.instructions.instruction_tag"
        )
        instr_tag_editor.add_from_import("podite", "Enum")
        if self.instr_tag_values == "anchor":
            tag_type = "U64"
            variant_type = "InstructionDiscriminant"
            instr_tag_editor.add_from_import(
                "solmate.anchor", "InstructionDiscriminant"
            )
        else:
            tag_type = self.instr_tag_values.split(":")[1]
            variant_type = "Variant"
            instr_tag_editor.add_from_import("podite", "Variant")

        instr_tag_editor.add_from_import("podite", "pod")
        instr_tag_editor.add_from_import("podite", tag_type)
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

    def generate_events(self):
        if not self.idl.events:
            return

        # TODO implement code generation for events
        print("Skipping events...")

    def generate_errors(self):
        if not self.idl.errors:
            return

        code = ["@pod\n", "class Error(Enum[U64]):\n"]
        for error in self.idl.errors:
            error_name = pascal_to_snake(error.name).upper()
            code.append(
                f'    {error_name} = Variant({error.code}, field="{error.msg}")\n'
            )

        editor = self.get_editor(f"{self.root_module}.errors")
        editor.add_from_import("podite", "pod")
        editor.add_from_import("podite", "Enum")
        editor.add_from_import("podite", "Variant")
        editor.add_from_import("podite", "U64")
        if editor.set_with_lock("errors", code):
            editor.add_lines(
                "\n",
                "    @classmethod\n",
                "    def to_bytes(cls, obj, **kwargs):\n",
                '        return cls.pack(obj, converter="bytes", **kwargs)\n',
                "\n",
                "    @classmethod\n",
                "    def from_bytes(cls, raw, **kwargs):\n",
                '        return cls.unpack(raw, converter="bytes", **kwargs)\n',
            )

        self._package_editor.add_from_import(f"{self.root_module}.errors", "Error")

    def generate_state(self):
        if not self.idl.state:
            return

        # TODO implement code generation for state
        print("Skipping state...")

    def generate_code(self, check_missing_types=False):
        self._package_editor = self.get_editor(self.root_module, is_file=False)

        self.generate_addresses()
        self.generate_types()
        self.generate_constants()
        self.generate_accounts()
        self.generate_instructions()
        self.generate_events()
        self.generate_errors()
        self.generate_state()

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


#########################
# Common external types #
#########################


def usize_type(editor: CodeEditor):
    editor.add_from_import("solmate.dtypes", "Usize")
    return "Usize"


def unix_timestamp_type(editor: CodeEditor):
    editor.add_from_import("solmate.dtypes", "UnixTimestamp")
    return "UnixTimestamp"


def program_error_type(editor: CodeEditor):
    editor.add_from_import("solmate.dtypes", "ProgramError")
    return "ProgramError"


def cli(
    idl_path: str,
    addresses: Dict[str, str],
    source_path: str,
    root_module: str,
    skip_types: Set[str],
    default_accounts: Dict[str, str],
    instr_tag_values: Literal["anchor", "incremental"],
    accnt_tag_values: Literal["anchor", "incremental"],
    external_types: Dict[str, Callable[[CodeEditor], str]] = None,
):
    idl = Idl.from_json_file(idl_path)
    idl.types = list(filter(lambda x: x.name not in skip_types, idl.types))

    external_types = {
        "usize": usize_type,
        "UnixTimestamp": unix_timestamp_type,
        "ProgramError": program_error_type,
    }.update(external_types if external_types is not None else {})

    print(f"Generating code for {idl_path}...")
    codegen = CodeGen(
        idl=idl,
        addresses=addresses,
        root_module=root_module,
        source_path=source_path,
        external_types=external_types,
        default_accounts=default_accounts,
        instr_tag_values=instr_tag_values,
        accnt_tag_values=accnt_tag_values,
        skip_types=skip_types,
    )
    codegen.generate_code(check_missing_types=not True)
    codegen.save_modules()
