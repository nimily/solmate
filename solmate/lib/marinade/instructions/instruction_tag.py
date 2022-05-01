# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Enum,
    U64,
    pod,
)
from solmate.anchor import InstructionDiscriminant

# LOCK-END


# LOCK-BEGIN[instruction_tag]: DON'T MODIFY
@pod
class InstructionTag(Enum[U64]):
    INITIALIZE = InstructionDiscriminant()
    CHANGE_AUTHORITY = InstructionDiscriminant()
    ADD_VALIDATOR = InstructionDiscriminant()
    REMOVE_VALIDATOR = InstructionDiscriminant()
    SET_VALIDATOR_SCORE = InstructionDiscriminant()
    CONFIG_VALIDATOR_SYSTEM = InstructionDiscriminant()
    DEPOSIT = InstructionDiscriminant()
    DEPOSIT_STAKE_ACCOUNT = InstructionDiscriminant()
    LIQUID_UNSTAKE = InstructionDiscriminant()
    ADD_LIQUIDITY = InstructionDiscriminant()
    REMOVE_LIQUIDITY = InstructionDiscriminant()
    SET_LP_PARAMS = InstructionDiscriminant()
    CONFIG_MARINADE = InstructionDiscriminant()
    ORDER_UNSTAKE = InstructionDiscriminant()
    CLAIM = InstructionDiscriminant()
    STAKE_RESERVE = InstructionDiscriminant()
    UPDATE_ACTIVE = InstructionDiscriminant()
    UPDATE_DEACTIVATED = InstructionDiscriminant()
    DEACTIVATE_STAKE = InstructionDiscriminant()
    EMERGENCY_UNSTAKE = InstructionDiscriminant()
    MERGE_STAKES = InstructionDiscriminant()
    # LOCK-END
