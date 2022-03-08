# LOCK-BEGIN[imports]: DON'T MODIFY
import solmate.lib.system_program

from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from pod import (
    BYTES_CATALOG,
    U64,
)
from typing import (
    List,
    Optional,
    Union,
)
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(transfer_with_seed)]: DON'T MODIFY
@dataclass
class TransferWithSeedIx:
    program_id: PublicKey

    # account metas
    from_pubkey: AccountMeta
    from_base: AccountMeta
    to_pubkey: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    lamports: U64
    fromSeed: str
    fromOwner: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.from_pubkey)
        keys.append(self.from_base)
        keys.append(self.to_pubkey)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.TRANSFER_WITH_SEED))
        buffer.write(BYTES_CATALOG.pack(U64, self.lamports))
        buffer.write(BYTES_CATALOG.pack(str, self.fromSeed))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.fromOwner))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(transfer_with_seed)]: DON'T MODIFY
def transfer_with_seed(
    from_pubkey: Union[str, PublicKey, AccountMeta],
    from_base: Union[str, PublicKey, AccountMeta],
    to_pubkey: Union[str, PublicKey, AccountMeta],
    lamports: U64,
    fromSeed: str,
    fromOwner: PublicKey,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = solmate.lib.system_program.PROGRAM_ID

    if isinstance(from_pubkey, (str, PublicKey)):
        from_pubkey = to_account_meta(
            from_pubkey,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(from_base, (str, PublicKey)):
        from_base = to_account_meta(
            from_base,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(to_pubkey, (str, PublicKey)):
        to_pubkey = to_account_meta(
            to_pubkey,
            is_signer=False,
            is_writable=True,
        )

    return TransferWithSeedIx(
        program_id=program_id,
        from_pubkey=from_pubkey,
        from_base=from_base,
        to_pubkey=to_pubkey,
        remaining_accounts=remaining_accounts,
        lamports=lamports,
        fromSeed=fromSeed,
        fromOwner=fromOwner,
    ).to_instruction()

# LOCK-END
