from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from solana.sysvar import SYSVAR_RENT_PUBKEY

from solmate.programs.token_program import instructions as ixs
from tests.programs.utils import get_pubkey, assert_ix_equal


def test_initialize_mint():
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
