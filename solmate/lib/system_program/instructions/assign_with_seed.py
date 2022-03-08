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


# LOCK-BEGIN[ix_cls(assign_with_seed)]: DON'T MODIFY
@dataclass
class AssignWithSeedIx:
    program_id: PublicKey

    # account metas
    address: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    base: PublicKey
    seed: str
    owner: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.address)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ASSIGN_WITH_SEED))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.base))
        buffer.write(BYTES_CATALOG.pack(str, self.seed))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.owner))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(assign_with_seed)]: DON'T MODIFY
def assign_with_seed(
    address: Union[str, PublicKey, AccountMeta],
    base: PublicKey,
    seed: str,
    owner: PublicKey,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = solmate.lib.system_program.PROGRAM_ID

    if isinstance(address, (str, PublicKey)):
        address = to_account_meta(
            address,
            is_signer=False,
            is_writable=True,
        )

    return AssignWithSeedIx(
        program_id=program_id,
        address=address,
        remaining_accounts=remaining_accounts,
        base=base,
        seed=seed,
        owner=owner,
    ).to_instruction()

# LOCK-END