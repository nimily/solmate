# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from podite import (
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
    PROGRAM_ID,
    RESERVE_PDA,
)
from solana.sysvar import (
    SYSVAR_CLOCK_PUBKEY as CLOCK,
    SYSVAR_RENT_PUBKEY as RENT,
)
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(deactivate_stake)]: DON'T MODIFY
@dataclass
class DeactivateStakeIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    reserve_pda: AccountMeta
    validator_list: AccountMeta
    stake_list: AccountMeta
    stake_account: AccountMeta
    stake_deposit_authority: AccountMeta
    split_stake_account: AccountMeta
    split_stake_rent_payer: AccountMeta
    clock: AccountMeta
    rent: AccountMeta
    epoch_schedule: AccountMeta
    stake_history: AccountMeta
    system_program: AccountMeta
    stake_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    stakeIndex: U32
    validatorIndex: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.reserve_pda)
        keys.append(self.validator_list)
        keys.append(self.stake_list)
        keys.append(self.stake_account)
        keys.append(self.stake_deposit_authority)
        keys.append(self.split_stake_account)
        keys.append(self.split_stake_rent_payer)
        keys.append(self.clock)
        keys.append(self.rent)
        keys.append(self.epoch_schedule)
        keys.append(self.stake_history)
        keys.append(self.system_program)
        keys.append(self.stake_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.DEACTIVATE_STAKE))
        buffer.write(BYTES_CATALOG.pack(U32, self.stakeIndex))
        buffer.write(BYTES_CATALOG.pack(U32, self.validatorIndex))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(deactivate_stake)]: DON'T MODIFY
def deactivate_stake(
    validator_list: Union[str, PublicKey, AccountMeta],
    stake_list: Union[str, PublicKey, AccountMeta],
    stake_account: Union[str, PublicKey, AccountMeta],
    stake_deposit_authority: Union[str, PublicKey, AccountMeta],
    split_stake_account: Union[str, PublicKey, AccountMeta],
    split_stake_rent_payer: Union[str, PublicKey, AccountMeta],
    epoch_schedule: Union[str, PublicKey, AccountMeta],
    stake_history: Union[str, PublicKey, AccountMeta],
    stake_program: Union[str, PublicKey, AccountMeta],
    stakeIndex: U32,
    validatorIndex: U32,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    reserve_pda: Union[str, PublicKey, AccountMeta] = RESERVE_PDA,
    clock: Union[str, PublicKey, AccountMeta] = CLOCK,
    rent: Union[str, PublicKey, AccountMeta] = RENT,
    system_program: Union[str, PublicKey, AccountMeta] = SYSTEM_PROGRAM,
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
    if isinstance(reserve_pda, (str, PublicKey)):
        reserve_pda = to_account_meta(
            reserve_pda,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(validator_list, (str, PublicKey)):
        validator_list = to_account_meta(
            validator_list,
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
    if isinstance(stake_deposit_authority, (str, PublicKey)):
        stake_deposit_authority = to_account_meta(
            stake_deposit_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(split_stake_account, (str, PublicKey)):
        split_stake_account = to_account_meta(
            split_stake_account,
            is_signer=True,
            is_writable=True,
        )
    if isinstance(split_stake_rent_payer, (str, PublicKey)):
        split_stake_rent_payer = to_account_meta(
            split_stake_rent_payer,
            is_signer=True,
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
    if isinstance(epoch_schedule, (str, PublicKey)):
        epoch_schedule = to_account_meta(
            epoch_schedule,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_history, (str, PublicKey)):
        stake_history = to_account_meta(
            stake_history,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_program, (str, PublicKey)):
        stake_program = to_account_meta(
            stake_program,
            is_signer=False,
            is_writable=False,
        )

    return DeactivateStakeIx(
        program_id=program_id,
        state=state,
        reserve_pda=reserve_pda,
        validator_list=validator_list,
        stake_list=stake_list,
        stake_account=stake_account,
        stake_deposit_authority=stake_deposit_authority,
        split_stake_account=split_stake_account,
        split_stake_rent_payer=split_stake_rent_payer,
        clock=clock,
        rent=rent,
        epoch_schedule=epoch_schedule,
        stake_history=stake_history,
        system_program=system_program,
        stake_program=stake_program,
        remaining_accounts=remaining_accounts,
        stakeIndex=stakeIndex,
        validatorIndex=validatorIndex,
    ).to_instruction()

# LOCK-END
