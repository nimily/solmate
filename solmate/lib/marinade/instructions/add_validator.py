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
from solana.sysvar import (
    SYSVAR_CLOCK_PUBKEY as CLOCK,
    SYSVAR_RENT_PUBKEY as RENT,
)
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(add_validator)]: DON'T MODIFY
@dataclass
class AddValidatorIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    manager_authority: AccountMeta
    validator_list: AccountMeta
    validator_vote: AccountMeta
    duplication_flag: AccountMeta
    rent_payer: AccountMeta
    clock: AccountMeta
    rent: AccountMeta
    system_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    score: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.manager_authority)
        keys.append(self.validator_list)
        keys.append(self.validator_vote)
        keys.append(self.duplication_flag)
        keys.append(self.rent_payer)
        keys.append(self.clock)
        keys.append(self.rent)
        keys.append(self.system_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ADD_VALIDATOR))
        buffer.write(BYTES_CATALOG.pack(U32, self.score))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(add_validator)]: DON'T MODIFY
def add_validator(
    manager_authority: Union[str, PublicKey, AccountMeta],
    validator_list: Union[str, PublicKey, AccountMeta],
    validator_vote: Union[str, PublicKey, AccountMeta],
    duplication_flag: Union[str, PublicKey, AccountMeta],
    rent_payer: Union[str, PublicKey, AccountMeta],
    score: U32,
    state: Union[str, PublicKey, AccountMeta] = STATE,
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
    if isinstance(manager_authority, (str, PublicKey)):
        manager_authority = to_account_meta(
            manager_authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(validator_list, (str, PublicKey)):
        validator_list = to_account_meta(
            validator_list,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(validator_vote, (str, PublicKey)):
        validator_vote = to_account_meta(
            validator_vote,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(duplication_flag, (str, PublicKey)):
        duplication_flag = to_account_meta(
            duplication_flag,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(rent_payer, (str, PublicKey)):
        rent_payer = to_account_meta(
            rent_payer,
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
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )

    return AddValidatorIx(
        program_id=program_id,
        state=state,
        manager_authority=manager_authority,
        validator_list=validator_list,
        validator_vote=validator_vote,
        duplication_flag=duplication_flag,
        rent_payer=rent_payer,
        clock=clock,
        rent=rent,
        system_program=system_program,
        remaining_accounts=remaining_accounts,
        score=score,
    ).to_instruction()

# LOCK-END
