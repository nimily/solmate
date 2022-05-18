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
from solmate.programs.token_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(mint_to)]: DON'T MODIFY
@dataclass
class MintToIx:
    program_id: PublicKey

    # account metas
    mint: AccountMeta
    account: AccountMeta
    authority: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    amount: U64

    def to_instruction(self):
        keys = []
        keys.append(self.mint)
        keys.append(self.account)
        keys.append(self.authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.MINT_TO))
        buffer.write(BYTES_CATALOG.pack(U64, self.amount))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(mint_to)]: DON'T MODIFY
def mint_to(
    mint: Union[str, PublicKey, AccountMeta],
    account: Union[str, PublicKey, AccountMeta],
    authority: Union[str, PublicKey, AccountMeta],
    amount: U64,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(mint, (str, PublicKey)):
        mint = to_account_meta(
            mint,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(account, (str, PublicKey)):
        account = to_account_meta(
            account,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(authority, (str, PublicKey)):
        authority = to_account_meta(
            authority,
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

    return MintToIx(
        program_id=program_id,
        mint=mint,
        account=account,
        authority=authority,
        remaining_accounts=remaining_accounts,
        amount=amount,
    ).to_instruction()


# LOCK-END
