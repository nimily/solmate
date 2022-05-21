# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Static,
    U64,
    pod,
)
from solana.publickey import PublicKey
from solmate.dtypes import COptional
from solmate.programs.token_program.types.account_state import AccountState

# LOCK-END


# LOCK-BEGIN[class(Account)]: DON'T MODIFY
@pod
class Account:
    mint: PublicKey
    owner: PublicKey
    amount: U64
    delegate: Static[COptional[PublicKey]]
    state: AccountState
    is_native: Static[COptional[U64]]
    delegated_amount: U64
    close_authority: Static[COptional[PublicKey]]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
