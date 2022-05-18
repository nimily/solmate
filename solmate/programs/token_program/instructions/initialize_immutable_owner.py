# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
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


# LOCK-BEGIN[ix_cls(initialize_immutable_owner)]: DON'T MODIFY
@dataclass
class InitializeImmutableOwnerIx:
    program_id: PublicKey

    # account metas
    account: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.account)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_IMMUTABLE_OWNER))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_immutable_owner)]: DON'T MODIFY
def initialize_immutable_owner(
    account: Union[str, PublicKey, AccountMeta],
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(account, (str, PublicKey)):
        account = to_account_meta(
            account,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(remaining_accounts, list):
        for i in range(len(remaining_accounts)):
            if isinstance(remaining_accounts[i], (str, PublicKey)):
                remaining_accounts[i] = to_account_meta(
                    remaining_accounts[i],
                    is_signer=False,
                    is_writable=False,
                )

    return InitializeImmutableOwnerIx(
        program_id=program_id,
        account=account,
        remaining_accounts=remaining_accounts,
    ).to_instruction()


# LOCK-END
