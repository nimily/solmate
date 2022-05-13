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


# LOCK-BEGIN[ix_cls(withdraw_nonce_account)]: DON'T MODIFY
@dataclass
class WithdrawNonceAccountIx:
    program_id: PublicKey

    # account metas
    nonce_pubkey: AccountMeta
    to_pubkey: AccountMeta
    recent_blockhashes_sysvar: AccountMeta
    rent_sysvar: AccountMeta
    authority: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    lamports: U64

    def to_instruction(self):
        keys = []
        keys.append(self.nonce_pubkey)
        keys.append(self.to_pubkey)
        keys.append(self.recent_blockhashes_sysvar)
        keys.append(self.rent_sysvar)
        keys.append(self.authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.WITHDRAW_NONCE_ACCOUNT))
        buffer.write(BYTES_CATALOG.pack(U64, self.lamports))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(withdraw_nonce_account)]: DON'T MODIFY
def withdraw_nonce_account(
    nonce_pubkey: Union[str, PublicKey, AccountMeta],
    to_pubkey: Union[str, PublicKey, AccountMeta],
    recent_blockhashes_sysvar: Union[str, PublicKey, AccountMeta],
    rent_sysvar: Union[str, PublicKey, AccountMeta],
    authority: Union[str, PublicKey, AccountMeta],
    lamports: U64,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: PublicKey = PROGRAM_ID,
):

    if isinstance(nonce_pubkey, (str, PublicKey)):
        nonce_pubkey = to_account_meta(
            nonce_pubkey,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(to_pubkey, (str, PublicKey)):
        to_pubkey = to_account_meta(
            to_pubkey,
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

    if isinstance(authority, (str, PublicKey)):
        authority = to_account_meta(
            authority,
            is_signer=True,
            is_writable=False,
        )

    return WithdrawNonceAccountIx(
        program_id=program_id,
        nonce_pubkey=nonce_pubkey,
        to_pubkey=to_pubkey,
        recent_blockhashes_sysvar=recent_blockhashes_sysvar,
        rent_sysvar=rent_sysvar,
        authority=authority,
        remaining_accounts=remaining_accounts,
        lamports=lamports,
    ).to_instruction()


# LOCK-END
