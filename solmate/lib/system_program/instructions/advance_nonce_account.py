# LOCK-BEGIN[imports]: DON'T MODIFY
import solmate.lib.system_program

from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from podite import BYTES_CATALOG
from typing import (
    List,
    Optional,
    Union,
)
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(advance_nonce_account)]: DON'T MODIFY
@dataclass
class AdvanceNonceAccountIx:
    program_id: PublicKey

    # account metas
    nonce_pubkey: AccountMeta
    recent_blockhashes_sysvar: AccountMeta
    authority: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.nonce_pubkey)
        keys.append(self.recent_blockhashes_sysvar)
        keys.append(self.authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ADVANCE_NONCE_ACCOUNT))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(advance_nonce_account)]: DON'T MODIFY
def advance_nonce_account(
    nonce_pubkey: Union[str, PublicKey, AccountMeta],
    recent_blockhashes_sysvar: Union[str, PublicKey, AccountMeta],
    authority: Union[str, PublicKey, AccountMeta],
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = solmate.lib.system_program.PROGRAM_ID

    if isinstance(nonce_pubkey, (str, PublicKey)):
        nonce_pubkey = to_account_meta(
            nonce_pubkey,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(recent_blockhashes_sysvar, (str, PublicKey)):
        recent_blockhashes_sysvar = to_account_meta(
            recent_blockhashes_sysvar,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(authority, (str, PublicKey)):
        authority = to_account_meta(
            authority,
            is_signer=True,
            is_writable=False,
        )

    return AdvanceNonceAccountIx(
        program_id=program_id,
        nonce_pubkey=nonce_pubkey,
        recent_blockhashes_sysvar=recent_blockhashes_sysvar,
        authority=authority,
        remaining_accounts=remaining_accounts,
    ).to_instruction()

# LOCK-END
