# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from solana.publickey import PublicKey
from solana.sysvar import SYSVAR_RENT_PUBKEY as RENT_SYSVAR
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solmate.programs.token_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(initialize_account)]: DON'T MODIFY
@dataclass
class InitializeAccountIx:
    program_id: PublicKey

    # account metas
    account: AccountMeta
    mint: AccountMeta
    owner_or_multisig: AccountMeta
    rent_sysvar: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.account)
        keys.append(self.mint)
        keys.append(self.owner_or_multisig)
        keys.append(self.rent_sysvar)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_ACCOUNT))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_account)]: DON'T MODIFY
def initialize_account(
    account: Union[str, PublicKey, AccountMeta],
    mint: Union[str, PublicKey, AccountMeta],
    owner_or_multisig: Union[str, PublicKey, AccountMeta],
    rent_sysvar: Union[str, PublicKey, AccountMeta] = RENT_SYSVAR,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(account, (str, PublicKey)):
        account = to_account_meta(
            account,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(mint, (str, PublicKey)):
        mint = to_account_meta(
            mint,
            is_signer=False,
            is_writable=False,
        )

    if isinstance(owner_or_multisig, (str, PublicKey)):
        owner_or_multisig = to_account_meta(
            owner_or_multisig,
            is_signer=False,
            is_writable=False,
        )

    if isinstance(rent_sysvar, (str, PublicKey)):
        rent_sysvar = to_account_meta(
            rent_sysvar,
            is_signer=False,
            is_writable=False,
        )

    if isinstance(remaining_accounts, list):
        for i in range(len(remaining_accounts)):
            if isinstance(remaining_accounts[i], (str, PublicKey)):
                remaining_accounts[i] = to_account_meta(
                    remaining_accounts[i],
                    is_signer=False,
                    is_writable=False,
                )

    return InitializeAccountIx(
        program_id=program_id,
        account=account,
        mint=mint,
        owner_or_multisig=owner_or_multisig,
        rent_sysvar=rent_sysvar,
        remaining_accounts=remaining_accounts,
    ).to_instruction()


# LOCK-END
