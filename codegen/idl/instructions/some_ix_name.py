# LOCK-BEGIN[imports]: DON'T MODIFY
import codegen.idl

from solana.publickey import PublicKey
from codegen.idl.types.array_of_enum_with_fields import ArrayOfEnumWithFields
from typing import (
    List,
    Optional,
)
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from io import BytesIO
from .instruction_tag import InstructionTag

# LOCK-END


# LOCK-BEGIN[instruction(some_ix_name)]: DON'T MODIFY
def some_ix_name(
    is_signer_true: PublicKey,
    is_mut_true: PublicKey,
    neither: PublicKey,
    both: PublicKey,
    params: ArrayOfEnumWithFields,
    remaining_accounts: Optional[List[AccountMeta]] = None,
):
    keys = [
        AccountMeta(pubkey=is_signer_true, is_signer=True, is_writable=False),
        AccountMeta(pubkey=is_mut_true, is_signer=False, is_writable=True),
        AccountMeta(pubkey=neither, is_signer=False, is_writable=False),
        AccountMeta(pubkey=both, is_signer=True, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys.extend(remaining_accounts)

    buffer = BytesIO()
    buffer.write(InstructionTag.to_bytes(InstructionTag.SOME_IX_NAME))
    buffer.write(ArrayOfEnumWithFields.to_bytes(params))

    return TransactionInstruction(
        keys=keys,
        program_id=codegen.idl.PROGRAM_ID,
        data=buffer.getvalue(),
    )

# LOCK-END
