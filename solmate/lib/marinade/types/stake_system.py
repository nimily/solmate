# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    U32,
    U64,
    U8,
    pod,
)
from solmate.lib.marinade.types.list import List

# LOCK-END


# LOCK-BEGIN[class(StakeSystem)]: DON'T MODIFY
@pod
class StakeSystem:
    stake_list: List
    delayed_unstake_cooling_down: U64
    stake_deposit_bump_seed: U8
    stake_withdraw_bump_seed: U8
    slots_for_stake_delta: U64
    last_stake_delta_epoch: U64
    min_stake: U64
    extra_stake_delta_runs: U32
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
