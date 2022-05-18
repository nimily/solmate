# LOCK-BEGIN[imports]: DON'T MODIFY
from ..constants import MAX_SIGNERS
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


# LOCK-BEGIN[ix_cls(close_account)]: DON'T MODIFY
@dataclass
class CloseAccountIx:
    program_id: PublicKey

    # account metas
    account: AccountMeta
    destination: AccountMeta
    account_owner: AccountMeta
    signers: Optional[List[AccountMeta]]
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.account)
        keys.append(self.destination)
        keys.append(self.account_owner)
        if self.signers is not None:
            keys.extend(self.signers)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.CLOSE_ACCOUNT))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(close_account)]: DON'T MODIFY
def close_account(
    account: Union[str, PublicKey, AccountMeta],
    destination: Union[str, PublicKey, AccountMeta],
    account_owner: Union[str, PublicKey, AccountMeta],
    signers: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(account, (str, PublicKey)):
        account = to_account_meta(
            account,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(destination, (str, PublicKey)):
        destination = to_account_meta(
            destination,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(account_owner, (str, PublicKey)):
        account_owner = to_account_meta(
            account_owner,
            is_signer=False if signers else True,
            is_writable=False,
        )

    if len(signers) > MAX_SIGNERS:
        raise ValueError(
            f"len(signers) cannot be bigger than {MAX_SIGNERS}, but was {len(signers)}"
        )

    if isinstance(signers, list):
        for i in range(len(signers)):
            if isinstance(signers[i], (str, PublicKey)):
                signers[i] = to_account_meta(
                    signers[i],
                    is_signer=True,
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

    return CloseAccountIx(
        program_id=program_id,
        account=account,
        destination=destination,
        account_owner=account_owner,
        signers=signers,
        remaining_accounts=remaining_accounts,
    ).to_instruction()


# LOCK-END
