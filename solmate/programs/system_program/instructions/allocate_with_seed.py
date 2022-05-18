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


# LOCK-BEGIN[ix_cls(allocate_with_seed)]: DON'T MODIFY
@dataclass
class AllocateWithSeedIx:
    program_id: PublicKey

    # account metas
    derived_pubkey: AccountMeta
    base_pubkey: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    base: PublicKey
    seed: str
    space: U64
    owner: PublicKey

    def to_instruction(self):
        keys = []
        keys.append(self.derived_pubkey)
        keys.append(self.base_pubkey)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.ALLOCATE_WITH_SEED))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.base))
        buffer.write(BYTES_CATALOG.pack(str, self.seed))
        buffer.write(BYTES_CATALOG.pack(U64, self.space))
        buffer.write(BYTES_CATALOG.pack(PublicKey, self.owner))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(allocate_with_seed)]: DON'T MODIFY
def allocate_with_seed(
    base: PublicKey,
    seed: str,
    space: U64,
    owner: PublicKey,
    derived_pubkey: Optional[Union[str, PublicKey, AccountMeta]] = None,
    base_pubkey: Optional[Union[str, PublicKey, AccountMeta]] = None,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):

    if derived_pubkey is None:
        derived_pubkey = PublicKey.create_with_seed(base, seed, owner)

    if isinstance(derived_pubkey, (str, PublicKey)):
        derived_pubkey = to_account_meta(
            derived_pubkey,
            is_signer=False,
            is_writable=True,
        )

    if base_pubkey is None:
        base_pubkey = base

    if isinstance(base_pubkey, (str, PublicKey)):
        base_pubkey = to_account_meta(
            base_pubkey,
            is_signer=True,
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

    return AllocateWithSeedIx(
        program_id=program_id,
        derived_pubkey=derived_pubkey,
        base_pubkey=base_pubkey,
        remaining_accounts=remaining_accounts,
        base=base,
        seed=seed,
        space=space,
        owner=owner,
    ).to_instruction()


# LOCK-END
