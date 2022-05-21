from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from solana.sysvar import SYSVAR_RENT_PUBKEY

from solmate.programs.token_program import instructions as ixs
from solmate.programs.token_program.accounts import Accounts
from solmate.programs.token_program.types import Mint, Account, AccountState
from tests.programs.utils import get_pubkey, assert_ix_equal


def test_initialize_mint__with_freeze_authority():
    key1 = get_pubkey(1)
    key2 = get_pubkey(2)
    key3 = get_pubkey(3)

    actual = ixs.initialize_mint(
        mint=key1,
        decimals=5,
        mint_authority=key2,
        freeze_authority=key3,
    )

    # generated using solana-py:
    # from spl.token.instructions import initialize_mint, InitializeMintParams
    # from spl.token.constants import TOKEN_PROGRAM_ID
    #
    # initialize_mint(
    #     InitializeMintParams(
    #         decimals=5,
    #         program_id=TOKEN_PROGRAM_ID,
    #         mint=key1,
    #         mint_authority=key2,
    #         freeze_authority=key3,
    #     )
    # )
    expect = TransactionInstruction(
        keys=[
            AccountMeta(pubkey=key1, is_signer=False, is_writable=True),
            AccountMeta(pubkey=SYSVAR_RENT_PUBKEY, is_signer=False, is_writable=False),
        ],
        program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
        data=b"\x00\x05\x819w\x0e\xa8}\x17_V\xa3Tf\xc3L~\xcc\xcb\x8d\x8a\x91\xb4\xee7"
        b"\xa2]\xf6\x0f[\x8f\xc9\xb3\x94\x01\xedI(\xc6(\xd1\xc2\xc6\xea\xe9\x038"
        b"\x90Y\x95a)Y':\\c\xf966\xc1F\x14\xac\x877\xd1",
    )

    assert_ix_equal(expect, actual)


def test_initialize_mint__without_freeze_authority():
    key1 = get_pubkey(1)
    key2 = get_pubkey(2)

    actual = ixs.initialize_mint(
        mint=key1,
        decimals=5,
        mint_authority=key2,
    )

    # generated using solana-py:
    # from spl.token.instructions import initialize_mint, InitializeMintParams
    # from spl.token.constants import TOKEN_PROGRAM_ID
    #
    # initialize_mint(
    #     InitializeMintParams(
    #         decimals=5,
    #         program_id=TOKEN_PROGRAM_ID,
    #         mint=key1,
    #         mint_authority=key2,
    #     )
    # )
    expect = TransactionInstruction(
        keys=[
            AccountMeta(pubkey=key1, is_signer=False, is_writable=True),
            AccountMeta(pubkey=SYSVAR_RENT_PUBKEY, is_signer=False, is_writable=False),
        ],
        program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
        data=b"\x00\x05\x819w\x0e\xa8}\x17_V\xa3Tf\xc3L~\xcc\xcb\x8d\x8a\x91\xb4\xee7"
        b"\xa2]\xf6\x0f[\x8f\xc9\xb3\x94\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00",
    )

    assert_ix_equal(expect, actual)


def test_accounts__mint_srm():
    # the following bytes sequence was generated using the following snippet. However, notice
    # that the supply will change over time and so the bytes won't match if called again.
    #
    # import base64
    #
    # from solana.publickey import PublicKey
    # from solana.rpc.api import Client
    #
    # client = Client("https://api.mainnet-beta.solana.com")
    #
    # srm = PublicKey("SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt")
    #
    # raw = base64.b64decode(client.get_account_info(srm)["result"]["value"]["data"][0])

    raw = (
        b"\x00\x00\x00\x00Y\xe4\xa73(\xf8\xa2\x07\\[\xb4\x0b\xb3\xce\x8ag\xd6d\x0c3\xf3V"
        b'>"j!\xc0\xef\xa5\x0b\x7fh\xf7;I\x84\x1a\x80#\x00\x06\x01\x00\x00\x00\x00Y\xe4'
        b'\xa73(\xf8\xa2\x07\\[\xb4\x0b\xb3\xce\x8ag\xd6d\x0c3\xf3V>"j!\xc0\xef\xa5\x0b'
        b"\x7fh"
    )

    obj: Accounts = Accounts.from_bytes(raw)

    assert obj.is_a(Accounts.MINT)

    mint: Mint = obj.field
    assert mint.is_initialized
    assert mint.decimals == 6
    assert mint.supply == 9992475561769975
    assert mint.mint_authority is None
    assert mint.freeze_authority is None


def test_accounts__mint_msol():
    # the following bytes sequence was generated using the following snippet. However, notice
    # that the supply will change over time and so the bytes won't match if called again.
    #
    # import base64
    #
    # from solana.publickey import PublicKey
    # from solana.rpc.api import Client
    #
    # client = Client("https://api.mainnet-beta.solana.com")
    #
    # msol = PublicKey("mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So")
    #
    # raw = base64.b64decode(client.get_account_info(msol)["result"]["value"]["data"][0])

    raw = (
        b'\x01\x00\x00\x00"()\xe8\x97g\xb2\x04<\x86\xd1\xb5\x1f16NZ\xda\xeb\x86\x1f\xd6.'
        b"z\x7fF\xbeM\xbb\xc5\\\xa4J\x1e8\x02\xd2J\x15\x00\t\x01\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    obj: Accounts = Accounts.from_bytes(raw)

    assert obj.is_a(Accounts.MINT)

    mint: Mint = obj.field
    assert mint.is_initialized
    assert mint.decimals == 9
    assert mint.supply == 5993240351743562
    assert mint.mint_authority == PublicKey(
        "3JLPCS1qM2zRw3Dp6V4hZnYHd4toMNPkNesXdX9tg6KM"
    )
    assert mint.freeze_authority is None


def test_accounts__account_msol_reserve():
    # the following bytes sequence was generated using the following snippet. However, notice
    # that the supply will change over time and so the bytes won't match if called again.
    #
    # import base64
    #
    # from solana.publickey import PublicKey
    # from solana.rpc.api import Client
    #
    # client = Client("https://api.mainnet-beta.solana.com")
    #
    # msol_reserve = PublicKey("Bcr3rbZq1g7FsPz8tawDzT6fCzN1pvADthcv3CtTpd3b")
    #
    # raw = base64.b64decode(client.get_account_info(msol_reserve)["result"]["value"]["data"][0])

    raw = (
        b"\x0bb\xba\x07Or,\x9dA\x14\xf2\xd8\xf7\n\x00\xc6`\x023{\x9b\xf9\x0c\x876W\xa6\xd2"
        b"\x01\xdbL\x80\x936\xb8\xc3\xee\xa8\xd3\xd2\x91\xf46$\x02\xd5t\x96[\x1a\xe6\xf2"
        b"\xf9\x0c'\xaf\xdc\xd3\x9d-V\x823\xf0\x8f \x8d\xd2\x88\x01\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    obj: Accounts = Accounts.from_bytes(raw)

    assert obj.is_a(Accounts.ACCOUNT)

    account: Account = obj.field

    assert account.mint == PublicKey("mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So")
    assert account.owner == PublicKey("AufL1ZuuAZoX7jBw8kECvjUYjfhWqZm13hbXeqnLMhFu")
    assert account.amount == 1687159644303
    assert account.delegate is None
    assert account.state.is_a(AccountState.INITIALIZED)
    assert not account.is_native
    assert account.delegated_amount == 0
    assert account.close_authority is None
