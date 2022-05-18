# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import (
    BYTES_CATALOG,
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


# LOCK-BEGIN[ix_cls(initialize_mint2)]: DON'T MODIFY
@dataclass
class InitializeMint2Ix:
    program_id: PublicKey

    # account metas
    mint: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    decimals: U8
    mint_authority: PublicKey
    freeze_authority: Optional[PublicKey]

    def to_instruction(self):
        keys = []
        keys.append(self.mint)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_MINT2))
        buffer.write(BYTES_CATALOG.pack(U8, self.decimals))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.mint_authority))
        buffer.write(BYTES_CATALOG.pack(Optional[PublicKey], self.freeze_authority))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_mint2)]: DON'T MODIFY
def initialize_mint2(
    mint: Union[str, PublicKey, AccountMeta],
    decimals: U8,
    mint_authority: PublicKey,
    freeze_authority: Optional[PublicKey],
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(mint, (str, PublicKey)):
        mint = to_account_meta(
            mint,
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

    return InitializeMint2Ix(
        program_id=program_id,
        mint=mint,
        remaining_accounts=remaining_accounts,
        decimals=decimals,
        mint_authority=mint_authority,
        freeze_authority=freeze_authority,
    ).to_instruction()


# LOCK-END
