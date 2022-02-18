# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    Enum,
    U8,
    Variant,
)

# LOCK-END


# LOCK-BEGIN[instruction_tag]: DON'T MODIFY
class InstructionTag(Enum[U8]):
    SOME_IX_NAME = Variant()
    # LOCK-END
