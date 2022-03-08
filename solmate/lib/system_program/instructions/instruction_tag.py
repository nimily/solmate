# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    Enum,
    U32,
    Variant,
    pod,
)

# LOCK-END


# LOCK-BEGIN[instruction_tag]: DON'T MODIFY
@pod
class InstructionTag(Enum[U32]):
    CREATE_ACCOUNT = Variant()
    ASSIGN = Variant()
    TRANSFER = Variant()
    CREATE_ACCOUNT_WITH_SEED = Variant()
    ADVANCE_NONCE_ACCOUNT = Variant()
    WITHDRAW_NONCE_ACCOUNT = Variant()
    INITIALIZE_NONCE_ACCOUNT = Variant()
    AUTHORIZE_NONCE_ACCOUNT = Variant()
    ALLOCATE = Variant()
    ALLOCATE_WITH_SEED = Variant()
    ASSIGN_WITH_SEED = Variant()
    TRANSFER_WITH_SEED = Variant()
    # LOCK-END
