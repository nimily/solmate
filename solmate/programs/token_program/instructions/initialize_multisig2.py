# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import (
    BYTES_CATALOG,
    U8,
)
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solmate.programs.token_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(initialize_multisig2)]: DON'T MODIFY
@dataclass
class InitializeMultisig2Ix:
    program_id: PublicKey

    # account metas
    multisig: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    m: U8

    def to_instruction(self):
        keys = []
        keys.append(self.multisig)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_MULTISIG2))
        buffer.write(BYTES_CATALOG.pack(U8, self.m))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_multisig2)]: DON'T MODIFY
def initialize_multisig2(
    multisig: Union[str, PublicKey, AccountMeta],
    m: U8,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(multisig, (str, PublicKey)):
        multisig = to_account_meta(
            multisig,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(remaining_accounts, list):
        for i in range(len(remaining_accounts)):
            if isinstance(remaining_accounts[i], (str, PublicKey)):
                remaining_accounts[i] = to_account_meta(
                    remaining_accounts[i],
                    is_signer=False,
                    is_writable=False,
                )

    return InitializeMultisig2Ix(
        program_id=program_id,
        multisig=multisig,
        remaining_accounts=remaining_accounts,
        m=m,
    ).to_instruction()


# LOCK-END
