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
    PROGRAM_ID,
)
from solana.sysvar import SYSVAR_CLOCK_PUBKEY as CLOCK
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(merge_stakes)]: DON'T MODIFY
@dataclass
class MergeStakesIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    stake_list: AccountMeta
    validator_list: AccountMeta
    destination_stake: AccountMeta
    source_stake: AccountMeta
    stake_deposit_authority: AccountMeta
    stake_withdraw_authority: AccountMeta
    operational_sol_account: AccountMeta
    clock: AccountMeta
    stake_history: AccountMeta
    stake_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    destinationStakeIndex: U32
    sourceStakeIndex: U32
    validatorIndex: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.stake_list)
        keys.append(self.validator_list)
        keys.append(self.destination_stake)
        keys.append(self.source_stake)
        keys.append(self.stake_deposit_authority)
        keys.append(self.stake_withdraw_authority)
        keys.append(self.operational_sol_account)
        keys.append(self.clock)
        keys.append(self.stake_history)
        keys.append(self.stake_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.MERGE_STAKES))
        buffer.write(BYTES_CATALOG.pack(U32, self.destinationStakeIndex))
        buffer.write(BYTES_CATALOG.pack(U32, self.sourceStakeIndex))
        buffer.write(BYTES_CATALOG.pack(U32, self.validatorIndex))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(merge_stakes)]: DON'T MODIFY
def merge_stakes(
    stake_list: Union[str, PublicKey, AccountMeta],
    validator_list: Union[str, PublicKey, AccountMeta],
    destination_stake: Union[str, PublicKey, AccountMeta],
    source_stake: Union[str, PublicKey, AccountMeta],
    stake_deposit_authority: Union[str, PublicKey, AccountMeta],
    stake_withdraw_authority: Union[str, PublicKey, AccountMeta],
    operational_sol_account: Union[str, PublicKey, AccountMeta],
    stake_history: Union[str, PublicKey, AccountMeta],
    stake_program: Union[str, PublicKey, AccountMeta],
    destinationStakeIndex: U32,
    sourceStakeIndex: U32,
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
    if isinstance(destination_stake, (str, PublicKey)):
        destination_stake = to_account_meta(
            destination_stake,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(source_stake, (str, PublicKey)):
        source_stake = to_account_meta(
            source_stake,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(stake_deposit_authority, (str, PublicKey)):
        stake_deposit_authority = to_account_meta(
            stake_deposit_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_withdraw_authority, (str, PublicKey)):
        stake_withdraw_authority = to_account_meta(
            stake_withdraw_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(operational_sol_account, (str, PublicKey)):
        operational_sol_account = to_account_meta(
            operational_sol_account,
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

    return MergeStakesIx(
        program_id=program_id,
        state=state,
        stake_list=stake_list,
        validator_list=validator_list,
        destination_stake=destination_stake,
        source_stake=source_stake,
        stake_deposit_authority=stake_deposit_authority,
        stake_withdraw_authority=stake_withdraw_authority,
        operational_sol_account=operational_sol_account,
        clock=clock,
        stake_history=stake_history,
        stake_program=stake_program,
        remaining_accounts=remaining_accounts,
        destinationStakeIndex=destinationStakeIndex,
        sourceStakeIndex=sourceStakeIndex,
        validatorIndex=validatorIndex,
    ).to_instruction()

# LOCK-END
