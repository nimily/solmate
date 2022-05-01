# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Option,
    U64,
    pod,
)
from solmate.lib.marinade.types.fee import Fee

# LOCK-END


# LOCK-BEGIN[class(ConfigMarinadeParams)]: DON'T MODIFY
@pod
class ConfigMarinadeParams:
    rewards_fee: Option[Fee]
    slots_for_stake_delta: Option[U64]
    min_stake: Option[U64]
    min_deposit: Option[U64]
    min_withdraw: Option[U64]
    staking_sol_cap: Option[U64]
    liquidity_sol_cap: Option[U64]
    auto_add_validator_enabled: Option[bool]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
