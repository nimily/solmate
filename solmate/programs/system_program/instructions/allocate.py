# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import (
    BYTES_CATALOG,
    U64,
)
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


# LOCK-BEGIN[ix_cls(allocate)]: DON'T MODIFY
@dataclass
class AllocateIx:
    program_id: PublicKey

    # account metas
    new_pubkey: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    space: U64

    def to_instruction(self):
        keys = []
        keys.append(self.new_pubkey)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ALLOCATE))
        buffer.write(BYTES_CATALOG.pack(U64, self.space))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(allocate)]: DON'T MODIFY
def allocate(
    new_pubkey: Union[str, PublicKey, AccountMeta],
    space: U64,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: PublicKey = PROGRAM_ID,
):

    if isinstance(new_pubkey, (str, PublicKey)):
        new_pubkey = to_account_meta(
            new_pubkey,
            is_signer=True,
            is_writable=True,
        )

    return AllocateIx(
        program_id=program_id,
        new_pubkey=new_pubkey,
        remaining_accounts=remaining_accounts,
        space=space,
    ).to_instruction()


# LOCK-END
