# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from podite import (
    BYTES_CATALOG,
    U64,
)
from typing import (
    List,
    Optional,
    Union,
)
from solmate.lib.marinade.types import Fee
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.lib.marinade.addrs import (
    MAIN_STATE as STATE,
    PROGRAM_ID,
)
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(set_lp_params)]: DON'T MODIFY
@dataclass
class SetLpParamsIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    admin_authority: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    minFee: Fee
    maxFee: Fee
    liquidityTarget: U64

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.admin_authority)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.SET_LP_PARAMS))
        buffer.write(BYTES_CATALOG.pack(Fee, self.minFee))
        buffer.write(BYTES_CATALOG.pack(Fee, self.maxFee))
        buffer.write(BYTES_CATALOG.pack(U64, self.liquidityTarget))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(set_lp_params)]: DON'T MODIFY
def set_lp_params(
    admin_authority: Union[str, PublicKey, AccountMeta],
    minFee: Fee,
    maxFee: Fee,
    liquidityTarget: U64,
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

    return SetLpParamsIx(
        program_id=program_id,
        state=state,
        admin_authority=admin_authority,
        remaining_accounts=remaining_accounts,
        minFee=minFee,
        maxFee=maxFee,
        liquidityTarget=liquidityTarget,
    ).to_instruction()

# LOCK-END
