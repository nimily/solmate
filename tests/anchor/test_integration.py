import json
from pathlib import Path

from solana.keypair import Keypair

from solmate.anchor import codegen
from solmate.anchor.idl import IdlField


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def test():
    root = str(get_project_root())
    codegen.cli(f"{root}/tests/anchor", root, "codegen", set())

    keypair = Keypair.generate()

    from codegen.idl.types import CallBackInfo
    info = CallBackInfo(keypair.public_key, 129)
    _bytes = CallBackInfo.to_bytes(info)
    round_tripped = CallBackInfo.from_bytes(_bytes)
    assert info == round_tripped

    from codegen.other.types.cross_idl_reference_type import CrossIdlReferenceType
    reference_type = CrossIdlReferenceType(keypair.public_key, info)
    _bytes = CrossIdlReferenceType.to_bytes(reference_type)
    round_tripped = CrossIdlReferenceType.from_bytes(_bytes)
    assert reference_type == round_tripped


def test2():
    raw = json.loads(""" 
    {
        "name": "callBackInfoField",
        "type": {
            "defined": "CallBackInfo"
        }
    }
    """)
    field = IdlField.from_dict(raw)

