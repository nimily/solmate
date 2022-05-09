# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import (
    BYTES_CATALOG,
    U64,
)
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solmate.lib.system_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(create_account)]: DON'T MODIFY
@dataclass
class CreateAccountIx:
    program_id: PublicKey

    # account metas
    from_pubkey: AccountMeta
    to_pubkey: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    lamports: U64
    space: U64
    owner: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.from_pubkey)
        keys.append(self.to_pubkey)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.CREATE_ACCOUNT))
        buffer.write(BYTES_CATALOG.pack(U64, self.lamports))
        buffer.write(BYTES_CATALOG.pack(U64, self.space))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.owner))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(create_account)]: DON'T MODIFY
def create_account(
    from_pubkey: Union[str, PublicKey, AccountMeta],
    to_pubkey: Union[str, PublicKey, AccountMeta],
    lamports: U64,
    space: U64,
    owner: PublicKey,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: PublicKey = PROGRAM_ID,
):

    if isinstance(from_pubkey, (str, PublicKey)):
        from_pubkey = to_account_meta(
            from_pubkey,
            is_signer=True,
            is_writable=True,
        )

    if isinstance(to_pubkey, (str, PublicKey)):
        to_pubkey = to_account_meta(
            to_pubkey,
            is_signer=True,
            is_writable=True,
        )

    return CreateAccountIx(
        program_id=program_id,
        from_pubkey=from_pubkey,
        to_pubkey=to_pubkey,
        remaining_accounts=remaining_accounts,
        lamports=lamports,
        space=space,
        owner=owner,
    ).to_instruction()


# LOCK-END
