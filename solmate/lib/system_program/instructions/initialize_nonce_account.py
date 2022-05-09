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


# LOCK-BEGIN[ix_cls(initialize_nonce_account)]: DON'T MODIFY
@dataclass
class InitializeNonceAccountIx:
    program_id: PublicKey

    # account metas
    nonce_pubkey: AccountMeta
    recent_blockhashes_sysvar: AccountMeta
    rent_sysvar: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    authority: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.nonce_pubkey)
        keys.append(self.recent_blockhashes_sysvar)
        keys.append(self.rent_sysvar)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_NONCE_ACCOUNT))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.authority))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_nonce_account)]: DON'T MODIFY
def initialize_nonce_account(
    nonce_pubkey: Union[str, PublicKey, AccountMeta],
    recent_blockhashes_sysvar: Union[str, PublicKey, AccountMeta],
    rent_sysvar: Union[str, PublicKey, AccountMeta],
    authority: PublicKey,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: PublicKey = PROGRAM_ID,
):

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

    if isinstance(rent_sysvar, (str, PublicKey)):
        rent_sysvar = to_account_meta(
            rent_sysvar,
            is_signer=False,
            is_writable=False,
        )

    return InitializeNonceAccountIx(
        program_id=program_id,
        nonce_pubkey=nonce_pubkey,
        recent_blockhashes_sysvar=recent_blockhashes_sysvar,
        rent_sysvar=rent_sysvar,
        remaining_accounts=remaining_accounts,
        authority=authority,
    ).to_instruction()


# LOCK-END
