import re
from typing import Union

from solana.publickey import PublicKey
from solana.transaction import AccountMeta


def camel_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def snake_to_camel(name):
    def _upper(m):
        return m.group(0)[1].upper()

    return re.sub(r"(?P<start>_[a-z])", _upper, name)


def pascal_to_snake(name):
    return camel_to_snake(name[0].lower() + name[1:])


def snake_to_pascal(name):
    pascal = snake_to_camel(name)
    return pascal[0].upper() + pascal[1:]


def kebab_to_snake(name):
    return re.sub("-", "_", name)


def snake_to_kebab(name):
    return re.sub("_", "-", name)


def to_account_meta(
    account: Union[str, PublicKey],
    is_signer: bool,
    is_writable: bool,
) -> AccountMeta:
    if isinstance(account, str):
        account = PublicKey(account)

    return AccountMeta(account, is_signer=is_signer, is_writable=is_writable)
