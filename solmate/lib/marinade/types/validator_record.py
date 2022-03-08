# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    U32,
    U64,
    U8,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(ValidatorRecord)]: DON'T MODIFY
@pod
class ValidatorRecord:
    validator_account: PublicKey
    active_balance: U64
    score: U32
    last_stake_delta_epoch: U64
    duplication_flag_bump_seed: U8
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
