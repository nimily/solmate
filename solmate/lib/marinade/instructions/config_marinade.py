# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from pod import BYTES_CATALOG
from typing import (
    List,
    Optional,
    Union,
)
from solmate.lib.marinade.types import ConfigMarinadeParams
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.lib.marinade.addrs import (
    MAIN_STATE as STATE,
    PROGRAM_ID,
)
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(config_marinade)]: DON'T MODIFY
@dataclass
class ConfigMarinadeIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    admin_authority: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: ConfigMarinadeParams

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.admin_authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.CONFIG_MARINADE))
        buffer.write(BYTES_CATALOG.pack(ConfigMarinadeParams, self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(config_marinade)]: DON'T MODIFY
def config_marinade(
    admin_authority: Union[str, PublicKey, AccountMeta],
    params: ConfigMarinadeParams,
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
    if isinstance(admin_authority, (str, PublicKey)):
        admin_authority = to_account_meta(
            admin_authority,
            is_signer=True,
            is_writable=False,
        )

    return ConfigMarinadeIx(
        program_id=program_id,
        state=state,
        admin_authority=admin_authority,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
