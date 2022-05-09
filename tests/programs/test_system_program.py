from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta

from solmate.programs.system_program import instructions as ixs
from tests.programs.utils import get_pubkey, assert_ix_equal


def test_create_account():
    key1 = get_pubkey(1)
    key2 = get_pubkey(2)
    owner = get_pubkey(3)

    actual = ixs.create_account(
        from_pubkey=key1,
        to_pubkey=key2,
        lamports=12457,
        space=17,
        owner=owner,
    )

    # generated using solana-py:
    # from solana.system_program import create_account, CreateAccountParams
    #
    # create_account(
    #     CreateAccountParams(
    #         key1,
    #         key2,
    #         lamports=12457,
    #         space=17,
    #         program_id=owner,
    #     )
    # )
    expect = TransactionInstruction(
        keys=[
            AccountMeta(
                pubkey=key1,
                is_signer=True,
                is_writable=True,
            ),
            AccountMeta(
                pubkey=key2,
                is_signer=True,
                is_writable=True,
            ),
        ],
        program_id=PublicKey("11111111111111111111111111111111"),
        data=b"\x00\x00\x00\x00\xa90\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\xed"
        b"I(\xc6(\xd1\xc2\xc6\xea\xe9\x038\x90Y\x95a)Y':\\c\xf966\xc1F\x14\xac\x877\xd1",
    )

    assert_ix_equal(expect, actual)


def test_assign():
    key1 = get_pubkey(1)
    owner = get_pubkey(2)

    actual = ixs.assign(
        pubkey=key1,
        owner=owner,
    )

    # generated using solana-py:
    # from solana.system_program import assign, AssignParams
    #
    # assign(
    #     AssignParams(
    #         key1,
    #         program_id=owner,
    #     )
    # )
    expect = TransactionInstruction(
        keys=[AccountMeta(pubkey=key1, is_signer=True, is_writable=True)],
        program_id=PublicKey("11111111111111111111111111111111"),
        data=b"\x01\x00\x00\x00\x819w\x0e\xa8}\x17_V\xa3Tf\xc3L~\xcc\xcb"
        b"\x8d\x8a\x91\xb4\xee7\xa2]\xf6\x0f[\x8f\xc9\xb3\x94",
    )

    assert_ix_equal(expect, actual)


def test_transfer():
    from_pubkey = get_pubkey(1)
    to_pubkey = get_pubkey(2)

    actual = ixs.transfer(
        from_pubkey=from_pubkey,
        to_pubkey=to_pubkey,
        lamports=54_000_000,
    )

    # generated using solana-py:
    # from tests.programs.utils import get_pubkey, assert_ix_equal
    # from solana.system_program import transfer, TransferParams
    #
    # transfer(
    #     TransferParams(
    #         from_pubkey,
    #         to_pubkey,
    #         lamports=54_000_000,
    #     )
    # )
    expect = TransactionInstruction(
        keys=[
            AccountMeta(pubkey=from_pubkey, is_signer=True, is_writable=True),
            AccountMeta(pubkey=to_pubkey, is_signer=False, is_writable=True),
        ],
        program_id=PublicKey("11111111111111111111111111111111"),
        data=b"\x02\x00\x00\x00\x80\xf97\x03\x00\x00\x00\x00",
    )

    assert_ix_equal(expect, actual)


def test_create_account_with_seed1():
    from_pubkey = get_pubkey(1)
    base = get_pubkey(2)
    owner = PublicKey("11111111111111111111111111111111")
    seed = "test-account-with-seed"
    derived = PublicKey.create_with_seed(base, seed, owner)

    actual = ixs.create_account_with_seed(
        from_pubkey=from_pubkey,
        base=base,
        seed=seed,
        lamports=63_000_000,
        space=123,
        owner=owner,
    )

    # manually generated. could be tested on local validator using:
    #
    # from solana.rpc.api import Client
    # from solana.transaction import Transaction
    # from tests.programs.utils import get_keypair
    #
    # client = Client()
    # from_keypair = get_keypair(1)
    # base_keypair = get_keypair(2)
    #
    # client.request_airdrop(from_keypair.public_key, 1_000_000_000)
    # client.request_airdrop(base_keypair.public_key, 1_000)  # just to make it exist
    #
    # tx = Transaction().add(actual)
    # client.send_transaction(tx, from_keypair, base_keypair)

    expect = TransactionInstruction(
        keys=[
            AccountMeta(pubkey=from_pubkey, is_signer=True, is_writable=True),
            AccountMeta(pubkey=derived, is_signer=False, is_writable=True),
            AccountMeta(pubkey=base, is_signer=True, is_writable=False),
        ],
        program_id=PublicKey("11111111111111111111111111111111"),
        data=b"\x03\x00\x00\x00\x819w\x0e\xa8}\x17_V\xa3Tf\xc3L~\xcc\xcb\x8d\x8a"
        b"\x91\xb4\xee7\xa2]\xf6\x0f[\x8f\xc9\xb3\x94\x16\x00\x00\x00\x00\x00"
        b"\x00\x00test-account-with-seed\xc0M\xc1\x03\x00\x00\x00\x00{\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00",
    )
    assert_ix_equal(expect, actual)


def test_create_account_with_seed2():
    from_pubkey = get_pubkey(1)
    base = from_pubkey
    owner = PublicKey("11111111111111111111111111111111")
    seed = "test-account-with-seed"
    derived = PublicKey.create_with_seed(base, seed, owner)

    actual = ixs.create_account_with_seed(
        from_pubkey=from_pubkey,
        base=base,
        seed=seed,
        lamports=63_000_000,
        space=123,
        owner=owner,
    )

    # manually generated. could be tested on local validator using:
    #
    # from solana.rpc.api import Client
    # from solana.transaction import Transaction
    # from tests.programs.utils import get_keypair
    #
    # client = Client()
    # from_keypair = get_keypair(1)
    #
    # client.request_airdrop(from_keypair.public_key, 1_000_000_000)
    #
    # tx = Transaction().add(actual)
    # client.send_transaction(tx, from_keypair)

    expect = TransactionInstruction(
        keys=[
            AccountMeta(pubkey=from_pubkey, is_signer=True, is_writable=True),
            AccountMeta(pubkey=derived, is_signer=False, is_writable=True),
        ],
        program_id=owner,
        data=b"\x03\x00\x00\x00\x8a\x88\xe3\xddt\t\xf1\x95\xfdR\xdb-<\xba]r\xcag"
        b"\t\xbf\x1d\x94\x12\x1b\xf3t\x88\x01\xb4\x0fo\\\x16\x00\x00\x00\x00"
        b"\x00\x00\x00test-account-with-seed\xc0M\xc1\x03\x00\x00\x00\x00{\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00",
    )
    assert_ix_equal(expect, actual)
