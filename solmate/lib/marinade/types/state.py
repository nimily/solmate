# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    U64,
    U8,
    pod,
)
from solana.publickey import PublicKey
from solmate.lib.marinade.types.fee import Fee
from solmate.lib.marinade.types.stake_system import StakeSystem
from solmate.lib.marinade.types.validator_system import ValidatorSystem
from solmate.lib.marinade.types.liq_pool import LiqPool

# LOCK-END


# LOCK-BEGIN[class(State)]: DON'T MODIFY
@pod
class State:
    msol_mint: PublicKey
    admin_authority: PublicKey
    operational_sol_account: PublicKey
    treasury_msol_account: PublicKey
    reserve_bump_seed: U8
    msol_mint_authority_bump_seed: U8
    rent_exempt_for_token_acc: U64
    reward_fee: Fee
    stake_system: StakeSystem
    validator_system: ValidatorSystem
    liq_pool: LiqPool
    available_reserve_balance: U64
    msol_supply: U64
    msol_price: U64
    circulating_ticket_count: U64
    circulating_ticket_balance: U64
    lent_from_reserve: U64
    min_deposit: U64
    min_withdraw: U64
    staking_sol_cap: U64
    emergency_cooling_down: U64
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
