# LOCK-BEGIN[imports]: DON'T MODIFY
import codegen.other.types as types

from solana.publickey import PublicKey
from solmate import get_pid_or_default

# LOCK-END


# LOCK-BEGIN[program_id]: DON'T MODIFY
PROGRAM_ID = get_pid_or_default("other", PublicKey("4vY1e8Vu5NEeTdhD9NMUUq6MwzYmFL4kskzmJoeVRMGr"))
# LOCK-END
