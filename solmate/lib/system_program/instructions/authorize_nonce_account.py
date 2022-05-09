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
from solmate.lib.system_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

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
    new_authority: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.nonce_pubkey)
        keys.append(self.authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.AUTHORIZE_NONCE_ACCOUNT))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.new_authority))

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
    new_authority: PublicKey,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: PublicKey = PROGRAM_ID,
):

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
        new_authority=new_authority,
    ).to_instruction()


# LOCK-END
