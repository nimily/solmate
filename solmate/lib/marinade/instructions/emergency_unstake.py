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
)
from solana.sysvar import SYSVAR_CLOCK_PUBKEY as CLOCK
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(emergency_unstake)]: DON'T MODIFY
@dataclass
class EmergencyUnstakeIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    validator_manager_authority: AccountMeta
    validator_list: AccountMeta
    stake_list: AccountMeta
    stake_account: AccountMeta
    stake_deposit_authority: AccountMeta
    clock: AccountMeta
    stake_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    stakeIndex: U32
    validatorIndex: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.validator_manager_authority)
        keys.append(self.validator_list)
        keys.append(self.stake_list)
        keys.append(self.stake_account)
        keys.append(self.stake_deposit_authority)
        keys.append(self.clock)
        keys.append(self.stake_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.EMERGENCY_UNSTAKE))
        buffer.write(BYTES_CATALOG.pack(U32, self.stakeIndex))
        buffer.write(BYTES_CATALOG.pack(U32, self.validatorIndex))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(emergency_unstake)]: DON'T MODIFY
def emergency_unstake(
    validator_manager_authority: Union[str, PublicKey, AccountMeta],
    validator_list: Union[str, PublicKey, AccountMeta],
    stake_list: Union[str, PublicKey, AccountMeta],
    stake_account: Union[str, PublicKey, AccountMeta],
    stake_deposit_authority: Union[str, PublicKey, AccountMeta],
    stake_program: Union[str, PublicKey, AccountMeta],
    stakeIndex: U32,
    validatorIndex: U32,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    clock: Union[str, PublicKey, AccountMeta] = CLOCK,
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
    if isinstance(validator_manager_authority, (str, PublicKey)):
        validator_manager_authority = to_account_meta(
            validator_manager_authority,
            is_signer=True,
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
    if isinstance(clock, (str, PublicKey)):
        clock = to_account_meta(
            clock,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_program, (str, PublicKey)):
        stake_program = to_account_meta(
            stake_program,
            is_signer=False,
            is_writable=False,
        )

    return EmergencyUnstakeIx(
        program_id=program_id,
        state=state,
        validator_manager_authority=validator_manager_authority,
        validator_list=validator_list,
        stake_list=stake_list,
        stake_account=stake_account,
        stake_deposit_authority=stake_deposit_authority,
        clock=clock,
        stake_program=stake_program,
        remaining_accounts=remaining_accounts,
        stakeIndex=stakeIndex,
        validatorIndex=validatorIndex,
    ).to_instruction()

# LOCK-END
