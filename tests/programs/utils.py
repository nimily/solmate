from solana.keypair import Keypair
from solana.transaction import TransactionInstruction


def assert_ix_equal(expect, actual):
    assert isinstance(expect, TransactionInstruction), "expect should be an instruction"
    assert isinstance(actual, TransactionInstruction), "actual should be an instruction"

    assert (
        expect.program_id == actual.program_id
    ), f"different program ids [{expect.program_id}] != [{actual.program_id}]"

    assert len(expect.keys) == len(
        actual.keys
    ), f"different number of keys {len(expect.keys)} != {len(actual.keys)}"

    for i, (key1, key2) in enumerate(zip(expect.keys, actual.keys)):
        assert key1.pubkey == key2.pubkey, f"different addresses in key {i}"
        assert (
            key1.is_writable == key2.is_writable
        ), f"different is_writable flags in key {i}"
        assert key1.is_signer == key2.is_signer, f"different is_signer flags in key {i}"

    assert expect.data == actual.data, "different instruction data"


def get_keypair(i):
    assert i < 256
    return Keypair.from_seed(bytes([i] * 32))


def get_pubkey(i):
    return get_keypair(i).public_key
