# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    U32,
    U64,
    U8,
    pod,
)
from solmate.lib.marinade.types.list import List
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(ValidatorSystem)]: DON'T MODIFY
@pod
class ValidatorSystem:
    validator_list: List
    manager_authority: PublicKey
    total_validator_score: U32
    total_active_balance: U64
    auto_add_validator_enabled: U8
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
