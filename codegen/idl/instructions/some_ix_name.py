# LOCK-BEGIN[imports]: DON'T MODIFY
import codegen.idl

from .instruction_tag import InstructionTag
from codegen.idl.types import ArrayOfEnumWithFields
from dataclasses import dataclass
from io import BytesIO
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(some_ix_name)]: DON'T MODIFY
@dataclass
class SomeIxNameIx:
    program_id: PublicKey

    # account metas
    is_signer_true: AccountMeta
    is_mut_true: AccountMeta
    neither: AccountMeta
    both: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: ArrayOfEnumWithFields

    def to_instruction(self):
        keys = []
        keys.append(self.is_signer_true)
        keys.append(self.is_mut_true)
        keys.append(self.neither)
        keys.append(self.both)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.SOME_IX_NAME))
        buffer.write(ArrayOfEnumWithFields.to_bytes(self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(some_ix_name)]: DON'T MODIFY
def some_ix_name(
    is_signer_true: Union[str, PublicKey, AccountMeta],
    is_mut_true: Union[str, PublicKey, AccountMeta],
    neither: Union[str, PublicKey, AccountMeta],
    both: Union[str, PublicKey, AccountMeta],
    params: ArrayOfEnumWithFields,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
    **kwargs,
):
    if program_id is None:
        program_id = codegen.idl.PROGRAM_ID

    if isinstance(is_signer_true, (str, PublicKey)):
        is_signer_true = to_account_meta(
            is_signer_true,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(is_mut_true, (str, PublicKey)):
        is_mut_true = to_account_meta(
            is_mut_true,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(neither, (str, PublicKey)):
        neither = to_account_meta(
            neither,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(both, (str, PublicKey)):
        both = to_account_meta(
            both,
            is_signer=True,
            is_writable=True,
        )

    return SomeIxNameIx(
        program_id=program_id,
        is_signer_true=is_signer_true,
        is_mut_true=is_mut_true,
        neither=neither,
        both=both,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
