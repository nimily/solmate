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
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(set_validator_score)]: DON'T MODIFY
@dataclass
class SetValidatorScoreIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    manager_authority: AccountMeta
    validator_list: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    index: U32
    validatorVote: PublicKey
    score: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.manager_authority)
        keys.append(self.validator_list)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.SET_VALIDATOR_SCORE))
        buffer.write(BYTES_CATALOG.pack(U32, self.index))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.validatorVote))
        buffer.write(BYTES_CATALOG.pack(U32, self.score))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(set_validator_score)]: DON'T MODIFY
def set_validator_score(
    manager_authority: Union[str, PublicKey, AccountMeta],
    validator_list: Union[str, PublicKey, AccountMeta],
    index: U32,
    validatorVote: PublicKey,
    score: U32,
    state: Union[str, PublicKey, AccountMeta] = STATE,
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

    return SetValidatorScoreIx(
        program_id=program_id,
        state=state,
        manager_authority=manager_authority,
        validator_list=validator_list,
        remaining_accounts=remaining_accounts,
        index=index,
        validatorVote=validatorVote,
        score=score,
    ).to_instruction()

# LOCK-END
