# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from podite import BYTES_CATALOG
from typing import (
    List,
    Optional,
    Union,
)
from solmate.lib.marinade.types import InitializeData
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.lib.marinade.addrs import (
    LP_MINT,
    MAIN_STATE as STATE,
    MSOL_MINT,
    PROGRAM_ID,
    RESERVE_PDA,
    TREASURY_MSOL_ACCOUNT,
)
from solana.sysvar import (
    SYSVAR_CLOCK_PUBKEY as CLOCK,
    SYSVAR_RENT_PUBKEY as RENT,
)
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(initialize)]: DON'T MODIFY
@dataclass
class InitializeIx:
    program_id: PublicKey

    # account metas
    creator_authority: AccountMeta
    state: AccountMeta
    reserve_pda: AccountMeta
    stake_list: AccountMeta
    validator_list: AccountMeta
    msol_mint: AccountMeta
    operational_sol_account: AccountMeta
    lp_mint: AccountMeta
    sol_leg_pda: AccountMeta
    msol_leg: AccountMeta
    treasury_msol_account: AccountMeta
    clock: AccountMeta
    rent: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    data: InitializeData

    def to_instruction(self):
        keys = []
        keys.append(self.creator_authority)
        keys.append(self.state)
        keys.append(self.reserve_pda)
        keys.append(self.stake_list)
        keys.append(self.validator_list)
        keys.append(self.msol_mint)
        keys.append(self.operational_sol_account)
        keys.append(self.lp_mint)
        keys.append(self.sol_leg_pda)
        keys.append(self.msol_leg)
        keys.append(self.treasury_msol_account)
        keys.append(self.clock)
        keys.append(self.rent)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE))
        buffer.write(BYTES_CATALOG.pack(InitializeData, self.data))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(initialize)]: DON'T MODIFY
def initialize(
    creator_authority: Union[str, PublicKey, AccountMeta],
    stake_list: Union[str, PublicKey, AccountMeta],
    validator_list: Union[str, PublicKey, AccountMeta],
    operational_sol_account: Union[str, PublicKey, AccountMeta],
    sol_leg_pda: Union[str, PublicKey, AccountMeta],
    msol_leg: Union[str, PublicKey, AccountMeta],
    data: InitializeData,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    reserve_pda: Union[str, PublicKey, AccountMeta] = RESERVE_PDA,
    msol_mint: Union[str, PublicKey, AccountMeta] = MSOL_MINT,
    lp_mint: Union[str, PublicKey, AccountMeta] = LP_MINT,
    treasury_msol_account: Union[str, PublicKey, AccountMeta] = TREASURY_MSOL_ACCOUNT,
    clock: Union[str, PublicKey, AccountMeta] = CLOCK,
    rent: Union[str, PublicKey, AccountMeta] = RENT,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PROGRAM_ID

    if isinstance(creator_authority, (str, PublicKey)):
        creator_authority = to_account_meta(
            creator_authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(state, (str, PublicKey)):
        state = to_account_meta(
            state,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(reserve_pda, (str, PublicKey)):
        reserve_pda = to_account_meta(
            reserve_pda,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_list, (str, PublicKey)):
        stake_list = to_account_meta(
            stake_list,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(validator_list, (str, PublicKey)):
        validator_list = to_account_meta(
            validator_list,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(msol_mint, (str, PublicKey)):
        msol_mint = to_account_meta(
            msol_mint,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(operational_sol_account, (str, PublicKey)):
        operational_sol_account = to_account_meta(
            operational_sol_account,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(lp_mint, (str, PublicKey)):
        lp_mint = to_account_meta(
            lp_mint,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(sol_leg_pda, (str, PublicKey)):
        sol_leg_pda = to_account_meta(
            sol_leg_pda,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(msol_leg, (str, PublicKey)):
        msol_leg = to_account_meta(
            msol_leg,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(treasury_msol_account, (str, PublicKey)):
        treasury_msol_account = to_account_meta(
            treasury_msol_account,
            is_signer=False,
            is_writable=False,
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

    return InitializeIx(
        program_id=program_id,
        creator_authority=creator_authority,
        state=state,
        reserve_pda=reserve_pda,
        stake_list=stake_list,
        validator_list=validator_list,
        msol_mint=msol_mint,
        operational_sol_account=operational_sol_account,
        lp_mint=lp_mint,
        sol_leg_pda=sol_leg_pda,
        msol_leg=msol_leg,
        treasury_msol_account=treasury_msol_account,
        clock=clock,
        rent=rent,
        remaining_accounts=remaining_accounts,
        data=data,
    ).to_instruction()

# LOCK-END
