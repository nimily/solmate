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
    LIQ_POOL_MSOL_LEG,
    LIQ_POOL_SOL_LEG as LIQ_POOL_SOL_LEG_PDA,
    MAIN_STATE as STATE,
    MSOL_MINT,
    PROGRAM_ID,
    TREASURY_MSOL_ACCOUNT,
)
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.lib.token_program import PROGRAM_ID as TOKEN_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(liquid_unstake)]: DON'T MODIFY
@dataclass
class LiquidUnstakeIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    msol_mint: AccountMeta
    liq_pool_sol_leg_pda: AccountMeta
    liq_pool_msol_leg: AccountMeta
    treasury_msol_account: AccountMeta
    get_msol_from: AccountMeta
    get_msol_from_authority: AccountMeta
    transfer_sol_to: AccountMeta
    system_program: AccountMeta
    token_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    msolAmount: U64

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.msol_mint)
        keys.append(self.liq_pool_sol_leg_pda)
        keys.append(self.liq_pool_msol_leg)
        keys.append(self.treasury_msol_account)
        keys.append(self.get_msol_from)
        keys.append(self.get_msol_from_authority)
        keys.append(self.transfer_sol_to)
        keys.append(self.system_program)
        keys.append(self.token_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.LIQUID_UNSTAKE))
        buffer.write(BYTES_CATALOG.pack(U64, self.msolAmount))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(liquid_unstake)]: DON'T MODIFY
def liquid_unstake(
    get_msol_from: Union[str, PublicKey, AccountMeta],
    get_msol_from_authority: Union[str, PublicKey, AccountMeta],
    transfer_sol_to: Union[str, PublicKey, AccountMeta],
    msolAmount: U64,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    msol_mint: Union[str, PublicKey, AccountMeta] = MSOL_MINT,
    liq_pool_sol_leg_pda: Union[str, PublicKey, AccountMeta] = LIQ_POOL_SOL_LEG_PDA,
    liq_pool_msol_leg: Union[str, PublicKey, AccountMeta] = LIQ_POOL_MSOL_LEG,
    treasury_msol_account: Union[str, PublicKey, AccountMeta] = TREASURY_MSOL_ACCOUNT,
    system_program: Union[str, PublicKey, AccountMeta] = SYSTEM_PROGRAM,
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
    if isinstance(liq_pool_sol_leg_pda, (str, PublicKey)):
        liq_pool_sol_leg_pda = to_account_meta(
            liq_pool_sol_leg_pda,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(liq_pool_msol_leg, (str, PublicKey)):
        liq_pool_msol_leg = to_account_meta(
            liq_pool_msol_leg,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(treasury_msol_account, (str, PublicKey)):
        treasury_msol_account = to_account_meta(
            treasury_msol_account,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(get_msol_from, (str, PublicKey)):
        get_msol_from = to_account_meta(
            get_msol_from,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(get_msol_from_authority, (str, PublicKey)):
        get_msol_from_authority = to_account_meta(
            get_msol_from_authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(transfer_sol_to, (str, PublicKey)):
        transfer_sol_to = to_account_meta(
            transfer_sol_to,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(token_program, (str, PublicKey)):
        token_program = to_account_meta(
            token_program,
            is_signer=False,
            is_writable=False,
        )

    return LiquidUnstakeIx(
        program_id=program_id,
        state=state,
        msol_mint=msol_mint,
        liq_pool_sol_leg_pda=liq_pool_sol_leg_pda,
        liq_pool_msol_leg=liq_pool_msol_leg,
        treasury_msol_account=treasury_msol_account,
        get_msol_from=get_msol_from,
        get_msol_from_authority=get_msol_from_authority,
        transfer_sol_to=transfer_sol_to,
        system_program=system_program,
        token_program=token_program,
        remaining_accounts=remaining_accounts,
        msolAmount=msolAmount,
    ).to_instruction()

# LOCK-END
