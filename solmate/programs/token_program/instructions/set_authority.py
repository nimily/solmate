# LOCK-BEGIN[imports]: DON'T MODIFY
from ..constants import MAX_SIGNERS
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from io import BytesIO
from podite import (
    BYTES_CATALOG,
    Option,
)
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solmate.programs.token_program.addrs import PROGRAM_ID
from solmate.programs.token_program.types import AuthorityType
from solmate.utils import to_account_meta
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(set_authority)]: DON'T MODIFY
@dataclass
class SetAuthorityIx:
    program_id: PublicKey

    # account metas
    mint_or_account: AccountMeta
    source_owner: AccountMeta
    signers: Optional[List[AccountMeta]]
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    authority_type: AuthorityType
    new_authority: Option[PublicKey]

    def to_instruction(self):
        keys = []
        keys.append(self.mint_or_account)
        keys.append(self.source_owner)
        if self.signers is not None:
            keys.extend(self.signers)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.SET_AUTHORITY))
        buffer.write(BYTES_CATALOG.pack(AuthorityType, self.authority_type))
        buffer.write(BYTES_CATALOG.pack(Option[PublicKey], self.new_authority))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )


# LOCK-END


# LOCK-BEGIN[ix_fn(set_authority)]: DON'T MODIFY
def set_authority(
    mint_or_account: Union[str, PublicKey, AccountMeta],
    source_owner: Union[str, PublicKey, AccountMeta],
    authority_type: AuthorityType,
    new_authority: Option[PublicKey],
    signers: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    remaining_accounts: Optional[List[Union[str, PublicKey, AccountMeta]]] = None,
    program_id: PublicKey = PROGRAM_ID,
):
    if isinstance(mint_or_account, (str, PublicKey)):
        mint_or_account = to_account_meta(
            mint_or_account,
            is_signer=False,
            is_writable=True,
        )

    if isinstance(source_owner, (str, PublicKey)):
        source_owner = to_account_meta(
            source_owner,
            is_signer=False if signers else True,
            is_writable=False,
        )

    if len(signers) > MAX_SIGNERS:
        raise ValueError(
            f"len(signers) cannot be bigger than {MAX_SIGNERS}, but was {len(signers)}"
        )

    if isinstance(signers, list):
        for i in range(len(signers)):
            if isinstance(signers[i], (str, PublicKey)):
                signers[i] = to_account_meta(
                    signers[i],
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

    return SetAuthorityIx(
        program_id=program_id,
        mint_or_account=mint_or_account,
        source_owner=source_owner,
        signers=signers,
        remaining_accounts=remaining_accounts,
        authority_type=authority_type,
        new_authority=new_authority,
    ).to_instruction()


# LOCK-END
