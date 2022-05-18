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
from solmate.programs.token_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(initialize_account3)]: DON'T MODIFY
@dataclass
class InitializeAccount3Ix:
    program_id: PublicKey

    # account metas
    account: AccountMeta
    mint: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    owner: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.account)
        keys.append(self.mint)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_ACCOUNT3))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.owner))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_account3)]: DON'T MODIFY
def initialize_account3(
    account: Union[str, PublicKey, AccountMeta],
    mint: Union[str, PublicKey, AccountMeta],
    owner: PublicKey,
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

    if isinstance(remaining_accounts, list):
        for i in range(len(remaining_accounts)):
            if isinstance(remaining_accounts[i], (str, PublicKey)):
                remaining_accounts[i] = to_account_meta(
                    remaining_accounts[i],
                    is_signer=False,
                    is_writable=False,
                )

    return InitializeAccount3Ix(
        program_id=program_id,
        account=account,
        mint=mint,
        remaining_accounts=remaining_accounts,
        owner=owner,
    ).to_instruction()


# LOCK-END
