# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from pod import (
    BYTES_CATALOG,
    U32,
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
    MSOL_MINT_AUTHORITY,
    PROGRAM_ID,
    RESERVE_PDA,
    TREASURY_MSOL_ACCOUNT,
)
from solana.sysvar import SYSVAR_CLOCK_PUBKEY as CLOCK
from solmate.lib.token_program import PROGRAM_ID as TOKEN_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(update_active)]: DON'T MODIFY
@dataclass
class UpdateActiveIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    stake_list: AccountMeta
    stake_account: AccountMeta
    stake_withdraw_authority: AccountMeta
    reserve_pda: AccountMeta
    msol_mint: AccountMeta
    msol_mint_authority: AccountMeta
    treasury_msol_account: AccountMeta
    clock: AccountMeta
    stake_history: AccountMeta
    stake_program: AccountMeta
    token_program: AccountMeta
    validator_list: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    stakeIndex: U32
    validatorIndex: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.stake_list)
        keys.append(self.stake_account)
        keys.append(self.stake_withdraw_authority)
        keys.append(self.reserve_pda)
        keys.append(self.msol_mint)
        keys.append(self.msol_mint_authority)
        keys.append(self.treasury_msol_account)
        keys.append(self.clock)
        keys.append(self.stake_history)
        keys.append(self.stake_program)
        keys.append(self.token_program)
        keys.append(self.validator_list)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.UPDATE_ACTIVE))
        buffer.write(BYTES_CATALOG.pack(U32, self.stakeIndex))
        buffer.write(BYTES_CATALOG.pack(U32, self.validatorIndex))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(update_active)]: DON'T MODIFY
def update_active(
    stake_list: Union[str, PublicKey, AccountMeta],
    stake_account: Union[str, PublicKey, AccountMeta],
    stake_withdraw_authority: Union[str, PublicKey, AccountMeta],
    stake_history: Union[str, PublicKey, AccountMeta],
    stake_program: Union[str, PublicKey, AccountMeta],
    validator_list: Union[str, PublicKey, AccountMeta],
    stakeIndex: U32,
    validatorIndex: U32,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    reserve_pda: Union[str, PublicKey, AccountMeta] = RESERVE_PDA,
    msol_mint: Union[str, PublicKey, AccountMeta] = MSOL_MINT,
    msol_mint_authority: Union[str, PublicKey, AccountMeta] = MSOL_MINT_AUTHORITY,
    treasury_msol_account: Union[str, PublicKey, AccountMeta] = TREASURY_MSOL_ACCOUNT,
    clock: Union[str, PublicKey, AccountMeta] = CLOCK,
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
    if isinstance(stake_list, (str, PublicKey)):
        stake_list = to_account_meta(
            stake_list,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(stake_account, (str, PublicKey)):
        stake_account = to_account_meta(
            stake_account,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(stake_withdraw_authority, (str, PublicKey)):
        stake_withdraw_authority = to_account_meta(
            stake_withdraw_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(reserve_pda, (str, PublicKey)):
        reserve_pda = to_account_meta(
            reserve_pda,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(msol_mint, (str, PublicKey)):
        msol_mint = to_account_meta(
            msol_mint,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(msol_mint_authority, (str, PublicKey)):
        msol_mint_authority = to_account_meta(
            msol_mint_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(treasury_msol_account, (str, PublicKey)):
        treasury_msol_account = to_account_meta(
            treasury_msol_account,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(clock, (str, PublicKey)):
        clock = to_account_meta(
            clock,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_history, (str, PublicKey)):
        stake_history = to_account_meta(
            stake_history,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_program, (str, PublicKey)):
        stake_program = to_account_meta(
            stake_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(token_program, (str, PublicKey)):
        token_program = to_account_meta(
            token_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(validator_list, (str, PublicKey)):
        validator_list = to_account_meta(
            validator_list,
            is_signer=False,
            is_writable=True,
        )

    return UpdateActiveIx(
        program_id=program_id,
        state=state,
        stake_list=stake_list,
        stake_account=stake_account,
        stake_withdraw_authority=stake_withdraw_authority,
        reserve_pda=reserve_pda,
        msol_mint=msol_mint,
        msol_mint_authority=msol_mint_authority,
        treasury_msol_account=treasury_msol_account,
        clock=clock,
        stake_history=stake_history,
        stake_program=stake_program,
        token_program=token_program,
        validator_list=validator_list,
        remaining_accounts=remaining_accounts,
        stakeIndex=stakeIndex,
        validatorIndex=validatorIndex,
    ).to_instruction()

# LOCK-END
