import os
from pathlib import Path
from solana.publickey import PublicKey
from solana.keypair import Keypair

from solmate.anchor import codegen


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def test():
    root = str(get_project_root())
    print(root)
    codegen.cli(f"{root}/tests/anchor", root, "codegen", set())

    from codegen.idl.types import CallBackInfo
    keypair = Keypair.generate()
    info = CallBackInfo(keypair.public_key, 129)
    _bytes = CallBackInfo.to_bytes(info)
    round_tripped = CallBackInfo.from_bytes(_bytes)
    assert info == round_tripped
