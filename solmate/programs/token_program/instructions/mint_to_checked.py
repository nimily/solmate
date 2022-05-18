# LOCK-BEGIN[imports]: DON'T MODIFY
from ..constants import MAX_SIGNERS
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import (
    BYTES_CATALOG,
    U64,
    U8,
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


# LOCK-BEGIN[ix_cls(mint_to_checked)]: DON'T MODIFY
@dataclass
class MintToCheckedIx:
    program_id: PublicKey

    # account metas
    mint: AccountMeta
    account: AccountMeta
    mint_authority: AccountMeta
    signers: Optional[List[AccountMeta]]
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    amount: U64
    decimals: U8

    def to_instruction(self):
        keys = []
        keys.append(self.mint)
        keys.append(self.account)
        keys.append(self.mint_authority)
        if self.signers is not None:
            keys.extend(self.signers)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.MINT_TO_CHECKED))
        buffer.write(BYTES_CATALOG.pack(U64, self.amount))
        buffer.write(BYTES_CATALOG.pack(U8, self.decimals))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(mint_to_checked)]: DON'T MODIFY
def mint_to_checked(
    mint: Union[str, PublicKey, AccountMeta],
    account: Union[str, PublicKey, AccountMeta],
    mint_authority: Union[str, PublicKey, AccountMeta],
    amount: U64,
    decimals: U8,
    signers: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
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

    if isinstance(mint_authority, (str, PublicKey)):
        mint_authority = to_account_meta(
            mint_authority,
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

    return MintToCheckedIx(
        program_id=program_id,
        mint=mint,
        account=account,
        mint_authority=mint_authority,
        signers=signers,
        remaining_accounts=remaining_accounts,
        amount=amount,
        decimals=decimals,
    ).to_instruction()


# LOCK-END
