import os
from pathlib import Path

from solmate.anchor import codegen


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def test():
    root = str(get_project_root())
    print(root)
    codegen.cli(f"{root}/tests/anchor", root, "codegen", set())

    assert False
