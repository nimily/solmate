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
from solmate.programs.system_program.addrs import PROGRAM_ID
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(transfer_with_seed)]: DON'T MODIFY
@dataclass
class TransferWithSeedIx:
    program_id: PublicKey

    # account metas
    from_pubkey: AccountMeta
    base_pubkey: AccountMeta
    derived_pubkey: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    lamports: U64
    seed: str
    owner: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.from_pubkey)
        keys.append(self.base_pubkey)
        keys.append(self.derived_pubkey)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.TRANSFER_WITH_SEED))
        buffer.write(BYTES_CATALOG.pack(U64, self.lamports))
        buffer.write(BYTES_CATALOG.pack(str, self.seed))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.owner))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(transfer_with_seed)]: DON'T MODIFY
def transfer_with_seed(
    from_pubkey: Union[str, PublicKey, AccountMeta],
    base_pubkey: Union[str, PublicKey, AccountMeta],
    lamports: U64,
    seed: str,
    owner: PublicKey,
    derived_pubkey: Optional[Union[str, PublicKey, AccountMeta]] = None,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):

    if isinstance(from_pubkey, (str, PublicKey)):
        from_pubkey = to_account_meta(
            from_pubkey,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(base_pubkey, (str, PublicKey)):
        base_pubkey = to_account_meta(
            base_pubkey,
            is_signer=True,
            is_writable=False,
        )

    if derived_pubkey is None:
        derived_pubkey = PublicKey.create_with_seed(base_pubkey.pubkey, seed, owner)

    if isinstance(derived_pubkey, (str, PublicKey)):
        derived_pubkey = to_account_meta(
            derived_pubkey,
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

    return TransferWithSeedIx(
        program_id=program_id,
        from_pubkey=from_pubkey,
        base_pubkey=base_pubkey,
        derived_pubkey=derived_pubkey,
        remaining_accounts=remaining_accounts,
        lamports=lamports,
        seed=seed,
        owner=owner,
    ).to_instruction()


# LOCK-END
