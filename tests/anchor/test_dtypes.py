from podite import U32
from solmate.dtypes import Repeat


def test_repeat():
    actual = [0, 1, 1000, 2 ** 31]

    raw = b""
    for e in actual:
        raw += U32.to_bytes(e)

    repeat_type = Repeat[U32]
    expect = repeat_type.from_bytes(raw)

    for i, value in enumerate(actual):
        assert value == expect[i]

    # ring behavior
    for i, value in enumerate(actual):
        assert value == expect[i + 4]
