from typing import Dict, Set, Callable, Literal

from solmate.anchor import CodeGen
from solmate.anchor.codegen import InstructionCodeGen, usize_type, AccountsCodeGen
from solmate.anchor.editor import CodeEditor
from solmate.anchor.idl import Idl, IdlAccount, IdlType
from solmate.utils import camel_to_snake, pascal_to_snake

ALLOW_MULTISIG_KEY = "allowMultisig"


class TokenProgramInstructionCodeGen(InstructionCodeGen):
    def get_instr_accounts(self):
        accounts = self._flatten_accounts(self.instr.accounts)

        for account, _ in accounts:
            metadata = account.metadata or {}
            if metadata.get(ALLOW_MULTISIG_KEY, False):
                accounts.append(
                    (
                        IdlAccount(
                            name="signers",
                            is_mut=False,
                            is_signer=True,
                            is_optional=True,
                            is_array=True,
                        ),
                        "signers",
                    )
                )

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

    def get_default_value(self, editor, arg):
        if arg.type.is_a(IdlType.OPTION):
            return "None"
        return super().get_default_value(editor, arg)

    def generate_ix_func_key_preprocessor(self, account, account_name):
        metadata = account.metadata or {}
        if metadata.get(ALLOW_MULTISIG_KEY, False):

            self.editor.add_from_import("solmate.utils", "to_account_meta")

            return [
                f"    if isinstance({account_name}, (str, PublicKey)):\n",
                f"        {account_name} = to_account_meta(\n",
                f"            {account_name},\n",
                f"            is_signer=False if signers else {account.is_signer},\n",
                f"            is_writable={account.is_mut},\n",
                f"        )\n",
            ]
        elif account_name == "signers":
            length = metadata.get("length", None)
            conditions = []
            if length:
                # this condition happens for initialize_multisig and initialize_multisig2
                self.editor.add_from_import("..constants", "MIN_SIGNERS")
                self.editor.add_from_import("..constants", "MAX_SIGNERS")

                conditions += [
                    f"    if {length} < MIN_SIGNERS or {length} > MAX_SIGNERS:\n",
                    f"        raise ValueError(\n",
                    f'            f"{length} should be between {{MIN_SIGNERS}} and {{MAX_SIGNERS}}, but was {{len(signers)}}"\n',
                    f"        )\n",
                    f"\n",
                    f"    if len(signers) != {length}:\n",
                    f"        raise ValueError(\n",
                    f'            f"len(signers) should be {length}, but was {{len(signers)}}"\n',
                    f"        )\n",
                    f"\n",
                ]
            else:
                # this condition happens for any instruction that requires signers such as transfer, approve, etc
                self.editor.add_from_import("..constants", "MAX_SIGNERS")

                conditions += [
                    f"    if len(signers) > MAX_SIGNERS:\n",
                    f"        raise ValueError(\n",
                    f'            f"len(signers) cannot be bigger than {{MAX_SIGNERS}}, but was {{len(signers)}}"\n',
                    f"        )\n",
                    f"\n",
                ]
        else:
            conditions = []

        return conditions + super().generate_ix_func_key_preprocessor(
            account, account_name
        )


class TokenProgramAccountsCodeGen(AccountsCodeGen):
    def generate_accounts_cls_packing_logic(self):
        code = [
            "\n",
            "    @classmethod\n",
            "    def _from_bytes_partial(cls, buffer, **kwargs):\n",
            "        account_len = buffer.getbuffer().nbytes - buffer.tell()\n",
        ]

        self.module_editor.add_from_import("podite", "BYTES_CATALOG")
        for account in self.accounts:
            variant = pascal_to_snake(account.name).upper()
            code += [
                f"        if account_len == {account.name}.calc_max_size():\n",
                f"            obj = BYTES_CATALOG.unpack_partial({account.name}, buffer)\n",
                f"            return Accounts.{variant}(obj)\n",
                f"\n",
            ]

        return code


class TokenProgramCodeGen(CodeGen):
    def generate_instruction(self, module_editor, instr):
        return TokenProgramInstructionCodeGen(self, module_editor, instr).generate()

    def generate_accounts(self):
        return TokenProgramAccountsCodeGen(
            self, self._package_editor, self.idl.accounts
        ).generate()

    def get_type_as_string(
        self, field_type, editor, within_types, explicit_forward_ref=False
    ):
        if field_type.is_a(IdlType.OPTION):
            inner_type = super().get_type_as_string(
                field_type.field, editor, within_types, explicit_forward_ref
            )

            if within_types:
                editor.add_from_import("podite", "Static")
                editor.add_from_import("solmate.dtypes", "COptional")
                return f"Static[COptional[{inner_type}]]"
            else:
                editor.add_from_import("podite", "Static")
                editor.add_from_import("typing", "Optional")
                return f"Static[Optional[{inner_type}]]"

        return super().get_type_as_string(
            field_type, editor, within_types, explicit_forward_ref
        )


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

    if external_types is None:
        external_types = {}
    external_types["usize"] = usize_type

    print(f"Generating code for {idl_path}...")
    codegen = TokenProgramCodeGen(
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
