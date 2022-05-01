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
    LP_MINT,
    LP_MINT_AUTHORITY,
    MAIN_STATE as STATE,
    PROGRAM_ID,
)
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.lib.token_program import PROGRAM_ID as TOKEN_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(add_liquidity)]: DON'T MODIFY
@dataclass
class AddLiquidityIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    lp_mint: AccountMeta
    lp_mint_authority: AccountMeta
    liq_pool_msol_leg: AccountMeta
    liq_pool_sol_leg_pda: AccountMeta
    transfer_from: AccountMeta
    mint_to: AccountMeta
    system_program: AccountMeta
    token_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    lamports: U64

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.lp_mint)
        keys.append(self.lp_mint_authority)
        keys.append(self.liq_pool_msol_leg)
        keys.append(self.liq_pool_sol_leg_pda)
        keys.append(self.transfer_from)
        keys.append(self.mint_to)
        keys.append(self.system_program)
        keys.append(self.token_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ADD_LIQUIDITY))
        buffer.write(BYTES_CATALOG.pack(U64, self.lamports))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(add_liquidity)]: DON'T MODIFY
def add_liquidity(
    transfer_from: Union[str, PublicKey, AccountMeta],
    mint_to: Union[str, PublicKey, AccountMeta],
    lamports: U64,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    lp_mint: Union[str, PublicKey, AccountMeta] = LP_MINT,
    lp_mint_authority: Union[str, PublicKey, AccountMeta] = LP_MINT_AUTHORITY,
    liq_pool_msol_leg: Union[str, PublicKey, AccountMeta] = LIQ_POOL_MSOL_LEG,
    liq_pool_sol_leg_pda: Union[str, PublicKey, AccountMeta] = LIQ_POOL_SOL_LEG_PDA,
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
    if isinstance(lp_mint, (str, PublicKey)):
        lp_mint = to_account_meta(
            lp_mint,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(lp_mint_authority, (str, PublicKey)):
        lp_mint_authority = to_account_meta(
            lp_mint_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(liq_pool_msol_leg, (str, PublicKey)):
        liq_pool_msol_leg = to_account_meta(
            liq_pool_msol_leg,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(liq_pool_sol_leg_pda, (str, PublicKey)):
        liq_pool_sol_leg_pda = to_account_meta(
            liq_pool_sol_leg_pda,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(transfer_from, (str, PublicKey)):
        transfer_from = to_account_meta(
            transfer_from,
            is_signer=True,
            is_writable=True,
        )
    if isinstance(mint_to, (str, PublicKey)):
        mint_to = to_account_meta(
            mint_to,
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

    return AddLiquidityIx(
        program_id=program_id,
        state=state,
        lp_mint=lp_mint,
        lp_mint_authority=lp_mint_authority,
        liq_pool_msol_leg=liq_pool_msol_leg,
        liq_pool_sol_leg_pda=liq_pool_sol_leg_pda,
        transfer_from=transfer_from,
        mint_to=mint_to,
        system_program=system_program,
        token_program=token_program,
        remaining_accounts=remaining_accounts,
        lamports=lamports,
    ).to_instruction()

# LOCK-END
