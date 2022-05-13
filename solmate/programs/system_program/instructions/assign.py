# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import BYTES_CATALOG
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solmate.programs.system_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

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
    program_id: PublicKey = PROGRAM_ID,
):

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
