# LOCK-BEGIN[imports]: DON'T MODIFY
from ..constants import (
    MAX_SIGNERS,
    MIN_SIGNERS,
)
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import (
    BYTES_CATALOG,
    U8,
)
from solana.publickey import PublicKey
from solana.sysvar import SYSVAR_RENT_PUBKEY as RENT_SYSVAR
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


# LOCK-BEGIN[ix_cls(initialize_multisig)]: DON'T MODIFY
@dataclass
class InitializeMultisigIx:
    program_id: PublicKey

    # account metas
    multisig: AccountMeta
    rent_sysvar: AccountMeta
    signers: List[AccountMeta]
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    m: U8

    def to_instruction(self):
        keys = []
        keys.append(self.multisig)
        keys.append(self.rent_sysvar)
        keys.extend(self.signers)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_MULTISIG))
        buffer.write(BYTES_CATALOG.pack(U8, self.m))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_multisig)]: DON'T MODIFY
def initialize_multisig(
    multisig: Union[str, PublicKey, AccountMeta],
    signers: List[Union[str, PublicKey, AccountMeta]],
    m: U8,
    rent_sysvar: Union[str, PublicKey, AccountMeta] = RENT_SYSVAR,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(multisig, (str, PublicKey)):
        multisig = to_account_meta(
            multisig,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(rent_sysvar, (str, PublicKey)):
        rent_sysvar = to_account_meta(
            rent_sysvar,
            is_signer=False,
            is_writable=False,
        )

    if m < MIN_SIGNERS or m > MAX_SIGNERS:
        raise ValueError(
            f"m should be between {MIN_SIGNERS} and {MAX_SIGNERS}, but was {len(signers)}"
        )

    if len(signers) != m:
        raise ValueError(f"len(signers) should be m, but was {len(signers)}")

    for i in range(len(signers)):
        if isinstance(signers[i], (str, PublicKey)):
            signers[i] = to_account_meta(
                signers[i],
                is_signer=False,
                is_writable=False,
            )

    if isinstance(remaining_accounts, list):
        for i in range(len(remaining_accounts)):
            if isinstance(remaining_accounts[i], (str, PublicKey)):
                remaining_accounts[i] = to_account_meta(
                    remaining_accounts[i],
                    is_signer=False,
                    is_writable=False,
                )

    return InitializeMultisigIx(
        program_id=program_id,
        multisig=multisig,
        rent_sysvar=rent_sysvar,
        signers=signers,
        remaining_accounts=remaining_accounts,
        m=m,
    ).to_instruction()


# LOCK-END
