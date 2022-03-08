# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    U64,
    U8,
    pod,
)
from solana.publickey import PublicKey
from solmate.lib.marinade.types.fee import Fee

# LOCK-END


# LOCK-BEGIN[class(LiqPool)]: DON'T MODIFY
@pod
class LiqPool:
    lp_mint: PublicKey
    lp_mint_authority_bump_seed: U8
    sol_leg_bump_seed: U8
    msol_leg_authority_bump_seed: U8
    msol_leg: PublicKey
    lp_liquidity_target: U64
    lp_max_fee: Fee
    lp_min_fee: Fee
    treasury_cut: Fee
    lp_supply: U64
    lent_from_sol_leg: U64
    liquidity_sol_cap: U64
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
