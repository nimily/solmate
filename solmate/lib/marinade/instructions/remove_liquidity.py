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
    MAIN_STATE as STATE,
    PROGRAM_ID,
)
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.lib.token_program import PROGRAM_ID as TOKEN_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(remove_liquidity)]: DON'T MODIFY
@dataclass
class RemoveLiquidityIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    lp_mint: AccountMeta
    burn_from: AccountMeta
    burn_from_authority: AccountMeta
    transfer_sol_to: AccountMeta
    transfer_msol_to: AccountMeta
    liq_pool_sol_leg_pda: AccountMeta
    liq_pool_msol_leg: AccountMeta
    liq_pool_msol_leg_authority: AccountMeta
    system_program: AccountMeta
    token_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    tokens: U64

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.lp_mint)
        keys.append(self.burn_from)
        keys.append(self.burn_from_authority)
        keys.append(self.transfer_sol_to)
        keys.append(self.transfer_msol_to)
        keys.append(self.liq_pool_sol_leg_pda)
        keys.append(self.liq_pool_msol_leg)
        keys.append(self.liq_pool_msol_leg_authority)
        keys.append(self.system_program)
        keys.append(self.token_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.REMOVE_LIQUIDITY))
        buffer.write(BYTES_CATALOG.pack(U64, self.tokens))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(remove_liquidity)]: DON'T MODIFY
def remove_liquidity(
    burn_from: Union[str, PublicKey, AccountMeta],
    burn_from_authority: Union[str, PublicKey, AccountMeta],
    transfer_sol_to: Union[str, PublicKey, AccountMeta],
    transfer_msol_to: Union[str, PublicKey, AccountMeta],
    liq_pool_msol_leg_authority: Union[str, PublicKey, AccountMeta],
    tokens: U64,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    lp_mint: Union[str, PublicKey, AccountMeta] = LP_MINT,
    liq_pool_sol_leg_pda: Union[str, PublicKey, AccountMeta] = LIQ_POOL_SOL_LEG_PDA,
    liq_pool_msol_leg: Union[str, PublicKey, AccountMeta] = LIQ_POOL_MSOL_LEG,
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
    if isinstance(burn_from, (str, PublicKey)):
        burn_from = to_account_meta(
            burn_from,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(burn_from_authority, (str, PublicKey)):
        burn_from_authority = to_account_meta(
            burn_from_authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(transfer_sol_to, (str, PublicKey)):
        transfer_sol_to = to_account_meta(
            transfer_sol_to,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(transfer_msol_to, (str, PublicKey)):
        transfer_msol_to = to_account_meta(
            transfer_msol_to,
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
    if isinstance(liq_pool_msol_leg_authority, (str, PublicKey)):
        liq_pool_msol_leg_authority = to_account_meta(
            liq_pool_msol_leg_authority,
            is_signer=False,
            is_writable=False,
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

    return RemoveLiquidityIx(
        program_id=program_id,
        state=state,
        lp_mint=lp_mint,
        burn_from=burn_from,
        burn_from_authority=burn_from_authority,
        transfer_sol_to=transfer_sol_to,
        transfer_msol_to=transfer_msol_to,
        liq_pool_sol_leg_pda=liq_pool_sol_leg_pda,
        liq_pool_msol_leg=liq_pool_msol_leg,
        liq_pool_msol_leg_authority=liq_pool_msol_leg_authority,
        system_program=system_program,
        token_program=token_program,
        remaining_accounts=remaining_accounts,
        tokens=tokens,
    ).to_instruction()

# LOCK-END
