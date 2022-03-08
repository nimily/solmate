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


# LOCK-BEGIN[ix_cls(authorize_nonce_account)]: DON'T MODIFY
@dataclass
class AuthorizeNonceAccountIx:
    program_id: PublicKey

    # account metas
    nonce_pubkey: AccountMeta
    authority: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    newAuthority: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.nonce_pubkey)
        keys.append(self.authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.AUTHORIZE_NONCE_ACCOUNT))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.newAuthority))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(authorize_nonce_account)]: DON'T MODIFY
def authorize_nonce_account(
    nonce_pubkey: Union[str, PublicKey, AccountMeta],
    authority: Union[str, PublicKey, AccountMeta],
    newAuthority: PublicKey,
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
    if isinstance(authority, (str, PublicKey)):
        authority = to_account_meta(
            authority,
            is_signer=True,
            is_writable=False,
        )

    return AuthorizeNonceAccountIx(
        program_id=program_id,
        nonce_pubkey=nonce_pubkey,
        authority=authority,
        remaining_accounts=remaining_accounts,
        newAuthority=newAuthority,
    ).to_instruction()

# LOCK-END
