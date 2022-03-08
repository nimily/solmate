# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from pod import (
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
    MSOL_MINT_AUTHORITY,
    PROGRAM_ID,
    RESERVE_PDA,
)
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.lib.token_program import PROGRAM_ID as TOKEN_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(deposit)]: DON'T MODIFY
@dataclass
class DepositIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    msol_mint: AccountMeta
    liq_pool_sol_leg_pda: AccountMeta
    liq_pool_msol_leg: AccountMeta
    liq_pool_msol_leg_authority: AccountMeta
    reserve_pda: AccountMeta
    transfer_from: AccountMeta
    mint_to: AccountMeta
    msol_mint_authority: AccountMeta
    system_program: AccountMeta
    token_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    lamports: U64

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.msol_mint)
        keys.append(self.liq_pool_sol_leg_pda)
        keys.append(self.liq_pool_msol_leg)
        keys.append(self.liq_pool_msol_leg_authority)
        keys.append(self.reserve_pda)
        keys.append(self.transfer_from)
        keys.append(self.mint_to)
        keys.append(self.msol_mint_authority)
        keys.append(self.system_program)
        keys.append(self.token_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.DEPOSIT))
        buffer.write(BYTES_CATALOG.pack(U64, self.lamports))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(deposit)]: DON'T MODIFY
def deposit(
    liq_pool_msol_leg_authority: Union[str, PublicKey, AccountMeta],
    transfer_from: Union[str, PublicKey, AccountMeta],
    mint_to: Union[str, PublicKey, AccountMeta],
    lamports: U64,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    msol_mint: Union[str, PublicKey, AccountMeta] = MSOL_MINT,
    liq_pool_sol_leg_pda: Union[str, PublicKey, AccountMeta] = LIQ_POOL_SOL_LEG_PDA,
    liq_pool_msol_leg: Union[str, PublicKey, AccountMeta] = LIQ_POOL_MSOL_LEG,
    reserve_pda: Union[str, PublicKey, AccountMeta] = RESERVE_PDA,
    msol_mint_authority: Union[str, PublicKey, AccountMeta] = MSOL_MINT_AUTHORITY,
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
    if isinstance(liq_pool_msol_leg_authority, (str, PublicKey)):
        liq_pool_msol_leg_authority = to_account_meta(
            liq_pool_msol_leg_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(reserve_pda, (str, PublicKey)):
        reserve_pda = to_account_meta(
            reserve_pda,
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
    if isinstance(msol_mint_authority, (str, PublicKey)):
        msol_mint_authority = to_account_meta(
            msol_mint_authority,
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

    return DepositIx(
        program_id=program_id,
        state=state,
        msol_mint=msol_mint,
        liq_pool_sol_leg_pda=liq_pool_sol_leg_pda,
        liq_pool_msol_leg=liq_pool_msol_leg,
        liq_pool_msol_leg_authority=liq_pool_msol_leg_authority,
        reserve_pda=reserve_pda,
        transfer_from=transfer_from,
        mint_to=mint_to,
        msol_mint_authority=msol_mint_authority,
        system_program=system_program,
        token_program=token_program,
        remaining_accounts=remaining_accounts,
        lamports=lamports,
    ).to_instruction()

# LOCK-END
