# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    U64,
    pod,
)
from solmate.lib.marinade.types.fee import Fee

# LOCK-END


# LOCK-BEGIN[class(LiqPoolInitializeData)]: DON'T MODIFY
@pod
class LiqPoolInitializeData:
    lp_liquidity_target: U64
    lp_max_fee: Fee
    lp_min_fee: Fee
    lp_treasury_cut: Fee
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
