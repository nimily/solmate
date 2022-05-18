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


# LOCK-BEGIN[ix_cls(ui_amount_to_amount)]: DON'T MODIFY
@dataclass
class UiAmountToAmountIx:
    program_id: PublicKey

    # account metas
    mint: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    ui_amount: str

    def to_instruction(self):
        keys = []
        keys.append(self.mint)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.UI_AMOUNT_TO_AMOUNT))
        buffer.write(BYTES_CATALOG.pack(str, self.ui_amount))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(ui_amount_to_amount)]: DON'T MODIFY
def ui_amount_to_amount(
    mint: Union[str, PublicKey, AccountMeta],
    ui_amount: str,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
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

    return UiAmountToAmountIx(
        program_id=program_id,
        mint=mint,
        remaining_accounts=remaining_accounts,
        ui_amount=ui_amount,
    ).to_instruction()


# LOCK-END
