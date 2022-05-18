# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Enum,
    U8,
    Variant,
    pod,
)

# LOCK-END


# LOCK-BEGIN[instruction_tag]: DON'T MODIFY
@pod
class InstructionTag(Enum[U8]):
    INITIALIZE_MINT = Variant()
    INITIALIZE_ACCOUNT = Variant()
    INITIALIZE_MULTISIG = Variant()
    TRANSFER = Variant()
    APPROVE = Variant()
    REVOKE = Variant()
    SET_AUTHORITY = Variant()
    MINT_TO = Variant()
    BURN = Variant()
    CLOSE_ACCOUNT = Variant()
    FREEZE_ACCOUNT = Variant()
    THAW_ACCOUNT = Variant()
    TRANSFER_CHECKED = Variant()
    APPROVE_CHECKED = Variant()
    MINT_TO_CHECKED = Variant()
    BURN_CHECKED = Variant()
    INITIALIZE_ACCOUNT2 = Variant()
    SYNC_NATIVE = Variant()
    INITIALIZE_ACCOUNT3 = Variant()
    INITIALIZE_MULTISIG2 = Variant()
    INITIALIZE_MINT2 = Variant()
    GET_ACCOUNT_DATA_SIZE = Variant()
    INITIALIZE_IMMUTABLE_OWNER = Variant()
    AMOUNT_TO_UI_AMOUNT = Variant()
    UI_AMOUNT_TO_AMOUNT = Variant()
    # LOCK-END
