# LOCK-BEGIN[imports]: DON'T MODIFY
import solmate.lib.system_program

from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from pod import BYTES_CATALOG
from typing import (
    List,
    Optional,
    Union,
)
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(assign)]: DON'T MODIFY
@dataclass
class AssignIx:
    program_id: PublicKey

    # account metas
    pubkey: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    owner: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.pubkey)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ASSIGN))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.owner))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(assign)]: DON'T MODIFY
def assign(
    pubkey: Union[str, PublicKey, AccountMeta],
    owner: PublicKey,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = solmate.lib.system_program.PROGRAM_ID

    if isinstance(pubkey, (str, PublicKey)):
        pubkey = to_account_meta(
            pubkey,
            is_signer=True,
            is_writable=True,
        )

    return AssignIx(
        program_id=program_id,
        pubkey=pubkey,
        remaining_accounts=remaining_accounts,
        owner=owner,
    ).to_instruction()

# LOCK-END
