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


# LOCK-BEGIN[ix_cls(config_validator_system)]: DON'T MODIFY
@dataclass
class ConfigValidatorSystemIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    manager_authority: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    extraRuns: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.manager_authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.CONFIG_VALIDATOR_SYSTEM))
        buffer.write(BYTES_CATALOG.pack(U32, self.extraRuns))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(config_validator_system)]: DON'T MODIFY
def config_validator_system(
    manager_authority: Union[str, PublicKey, AccountMeta],
    extraRuns: U32,
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

    return ConfigValidatorSystemIx(
        program_id=program_id,
        state=state,
        manager_authority=manager_authority,
        remaining_accounts=remaining_accounts,
        extraRuns=extraRuns,
    ).to_instruction()

# LOCK-END
