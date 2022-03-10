# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    Enum,
    U64,
    pod,
)
from solmate.anchor import InstructionDiscriminant

# LOCK-END


# LOCK-BEGIN[instruction_tag]: DON'T MODIFY
@pod
class InstructionTag(Enum[U64]):
    SOME_IX_NAME = InstructionDiscriminant()
    # LOCK-END
