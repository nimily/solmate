from pathlib import Path

from solana.keypair import Keypair

from solmate.anchor import codegen


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def test():
    keypair = Keypair.generate()
    root = str(get_project_root())
    codegen.cli(f"{root}/tests/anchor", root, "codegen", set())

    from codegen.idl.types import CallBackInfo
    from codegen.other.types.cross_idl_reference_type import CrossIdlReferenceType

    info = CallBackInfo(keypair.public_key, 129)
    _bytes = CallBackInfo.to_bytes(info)
    round_tripped = CallBackInfo.from_bytes(_bytes)
    assert info == round_tripped

    reference_type = CrossIdlReferenceType(keypair.public_key, info)
    _bytes = CrossIdlReferenceType.to_bytes(reference_type)
    round_tripped = CrossIdlReferenceType.from_bytes(_bytes)
    assert reference_type == round_tripped
