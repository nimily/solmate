# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    U64,
    U8,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(StakeRecord)]: DON'T MODIFY
@pod
class StakeRecord:
    stake_account: PublicKey
    last_update_delegated_lamports: U64
    last_update_epoch: U64
    is_emergency_unstaking: U8
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
