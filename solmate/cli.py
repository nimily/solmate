import argparse
import os

from solmate.anchor import codegen

TAG_TYPES = [
    "anchor",
    "incremental",
    "incremental:U8",
    "incremental:U16",
    "incremental:U32",
    "incremental:U64",
    "incremental:U128",
]


def default_account_gen(name_, value_):
    def _default_account(editor):
        from_clause, import_clause = value_.rsplit(".", maxsplit=1)
        as_clause = name_.upper()
        if as_clause == import_clause:
            editor.add_from_import(from_clause, import_clause)
        else:
            editor.add_from_import(from_clause, import_clause, name_.upper())
        return name_.upper()

    return _default_account


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--idl", type=str, required=True)
    parser.add_argument("--addrs", nargs="+", type=str, required=True, default=[])
    parser.add_argument("--root-dir", type=str, required=True, default=os.getcwd())
    parser.add_argument("--module", type=str, required=True)
    parser.add_argument("--skip-types", nargs="+", required=False, default=[])
    parser.add_argument(
        "--default-accounts", nargs="+", type=str, required=False, default=[]
    )
    parser.add_argument(
        "--instruction-tag",
        choices=TAG_TYPES,
        default="anchor",
        required=False,
    )
    parser.add_argument(
        "--account-tag",
        choices=TAG_TYPES,
        default="anchor",
        required=False,
    )
    args = parser.parse_args()

    skip_types = set(args.skip_types)

    default_accounts = {}
    for acct in args.default_accounts:
        name, value = acct.split("=")
        if "." in value:

            default_accounts[name] = default_account_gen(name, value)
        else:
            default_accounts[name] = value

    addresses = {}
    for acct in args.addrs:
        name, value = acct.split("=")
        addresses[name] = value

    instruction_tag = args.instruction_tag
    if instruction_tag == "incremental":
        instruction_tag = "incremental:U8"

    account_tag = args.account_tag
    if account_tag == "incremental":
        account_tag = "incremental:U8"

    codegen.cli(
        args.idl,
        addresses,
        args.root_dir,
        args.module,
        skip_types,
        default_accounts,
        instruction_tag,
        account_tag,
    )


if __name__ == "__main__":
    main()
