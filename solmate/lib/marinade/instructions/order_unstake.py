# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from podite import (
    BYTES_CATALOG,
    U64,
)
from typing import (
    List,
    Optional,
    Union,
)
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.lib.marinade.addrs import (
    MAIN_STATE as STATE,
    MSOL_MINT,
    PROGRAM_ID,
)
from solana.sysvar import (
    SYSVAR_CLOCK_PUBKEY as CLOCK,
    SYSVAR_RENT_PUBKEY as RENT,
)
from solmate.lib.token_program import PROGRAM_ID as TOKEN_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(order_unstake)]: DON'T MODIFY
@dataclass
class OrderUnstakeIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    msol_mint: AccountMeta
    burn_msol_from: AccountMeta
    burn_msol_authority: AccountMeta
    new_ticket_account: AccountMeta
    clock: AccountMeta
    rent: AccountMeta
    token_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    msolAmount: U64

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.msol_mint)
        keys.append(self.burn_msol_from)
        keys.append(self.burn_msol_authority)
        keys.append(self.new_ticket_account)
        keys.append(self.clock)
        keys.append(self.rent)
        keys.append(self.token_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ORDER_UNSTAKE))
        buffer.write(BYTES_CATALOG.pack(U64, self.msolAmount))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(order_unstake)]: DON'T MODIFY
def order_unstake(
    burn_msol_from: Union[str, PublicKey, AccountMeta],
    burn_msol_authority: Union[str, PublicKey, AccountMeta],
    new_ticket_account: Union[str, PublicKey, AccountMeta],
    msolAmount: U64,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    msol_mint: Union[str, PublicKey, AccountMeta] = MSOL_MINT,
    clock: Union[str, PublicKey, AccountMeta] = CLOCK,
    rent: Union[str, PublicKey, AccountMeta] = RENT,
    token_program: Union[str, PublicKey, AccountMeta] = TOKEN_PROGRAM,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PROGRAM_ID

    if isinstance(state, (str, PublicKey)):
        state = to_account_meta(
            state,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(msol_mint, (str, PublicKey)):
        msol_mint = to_account_meta(
            msol_mint,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(burn_msol_from, (str, PublicKey)):
        burn_msol_from = to_account_meta(
            burn_msol_from,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(burn_msol_authority, (str, PublicKey)):
        burn_msol_authority = to_account_meta(
            burn_msol_authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(new_ticket_account, (str, PublicKey)):
        new_ticket_account = to_account_meta(
            new_ticket_account,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(clock, (str, PublicKey)):
        clock = to_account_meta(
            clock,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(rent, (str, PublicKey)):
        rent = to_account_meta(
            rent,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(token_program, (str, PublicKey)):
        token_program = to_account_meta(
            token_program,
            is_signer=False,
            is_writable=False,
        )

    return OrderUnstakeIx(
        program_id=program_id,
        state=state,
        msol_mint=msol_mint,
        burn_msol_from=burn_msol_from,
        burn_msol_authority=burn_msol_authority,
        new_ticket_account=new_ticket_account,
        clock=clock,
        rent=rent,
        token_program=token_program,
        remaining_accounts=remaining_accounts,
        msolAmount=msolAmount,
    ).to_instruction()

# LOCK-END
