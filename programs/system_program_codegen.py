from typing import Dict, Set, Callable, Literal

from solmate.anchor import CodeGen
from solmate.anchor.codegen import InstructionCodeGen
from solmate.anchor.editor import CodeEditor
from solmate.anchor.idl import Idl
from solmate.utils import camel_to_snake


class SystemProgramInstructionCodeGen(InstructionCodeGen):
    def get_default_account(self, editor, account_name):
        if self.instr_name == "transfer_with_seed" and account_name == "base_pubkey":
            # transfer_with_seed doesn't have "base" arg!!!
            return None

        if account_name in ("base_pubkey", "derived_pubkey"):
            return "None"

        return super().get_default_account(editor, account_name)

    def generate_ix_func_key_preprocessor(self, account, prefix):
        code = ["\n"]
        if account.field.name == "basePubkey":
            if self.instr_name != "transfer_with_seed":
                metadata = account.field.metadata or {}
                refer = metadata.get("set_if_different", None)
                if refer is not None:
                    refer = camel_to_snake(refer)
                    code += [
                        f"    if base_pubkey is None and base != {refer}.pubkey:\n"
                    ]
                else:
                    code += ["    if base_pubkey is None:\n"]

                code += [
                    "        base_pubkey = base\n",
                    "\n",
                ]
        elif account.field.name == "derivedPubkey":
            self.editor.add_from_import("solana.publickey", "PublicKey")

            if self.instr_name == "transfer_with_seed":
                code += [
                    f"    if derived_pubkey is None:\n",
                    f"        derived_pubkey = PublicKey.create_with_seed(base_pubkey.pubkey, seed, owner)\n",
                    "\n",
                ]
            else:
                code += [
                    f"    if derived_pubkey is None:\n",
                    f"        derived_pubkey = PublicKey.create_with_seed(base, seed, owner)\n",
                    "\n",
                ]

        code += super().generate_ix_func_key_preprocessor(account, prefix)

        return code


class SystemProgramCodeGen(CodeGen):
    def generate_instruction(self, module_editor, instr):
        return SystemProgramInstructionCodeGen(self, module_editor, instr).generate()


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

    print(f"Generating code for {idl_path}...")
    codegen = SystemProgramCodeGen(
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


if __name__ == "__main__":
    from solmate.cli import main

    main(cli)
