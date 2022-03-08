# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    U32,
    U64,
    pod,
)
from solana.publickey import PublicKey
from solmate.lib.marinade.types.fee import Fee
from solmate.lib.marinade.types.liq_pool_initialize_data import LiqPoolInitializeData

# LOCK-END


# LOCK-BEGIN[class(InitializeData)]: DON'T MODIFY
@pod
class InitializeData:
    admin_authority: PublicKey
    validator_manager_authority: PublicKey
    min_stake: U64
    reward_fee: Fee
    liq_pool: "LiqPoolInitializeData"
    additional_stake_record_space: U32
    additional_validator_record_space: U32
    slots_for_stake_delta: U64
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
