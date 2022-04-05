# LOCK-BEGIN[imports]: DON'T MODIFY
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from solana.publickey import PublicKey
from dataclasses import dataclass
from podite import (
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
    MSOL_MINT,
    MSOL_MINT_AUTHORITY,
    PROGRAM_ID,
    STAKE_AUTHORITY,
)
from solana.sysvar import (
    SYSVAR_CLOCK_PUBKEY as CLOCK,
    SYSVAR_RENT_PUBKEY as RENT,
)
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.lib.token_program import PROGRAM_ID as TOKEN_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(deposit_stake_account)]: DON'T MODIFY
@dataclass
class DepositStakeAccountIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    validator_list: AccountMeta
    stake_list: AccountMeta
    stake_account: AccountMeta
    stake_authority: AccountMeta
    duplication_flag: AccountMeta
    rent_payer: AccountMeta
    msol_mint: AccountMeta
    mint_to: AccountMeta
    msol_mint_authority: AccountMeta
    clock: AccountMeta
    rent: AccountMeta
    system_program: AccountMeta
    token_program: AccountMeta
    stake_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    validatorIndex: U32

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.validator_list)
        keys.append(self.stake_list)
        keys.append(self.stake_account)
        keys.append(self.stake_authority)
        keys.append(self.duplication_flag)
        keys.append(self.rent_payer)
        keys.append(self.msol_mint)
        keys.append(self.mint_to)
        keys.append(self.msol_mint_authority)
        keys.append(self.clock)
        keys.append(self.rent)
        keys.append(self.system_program)
        keys.append(self.token_program)
        keys.append(self.stake_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.DEPOSIT_STAKE_ACCOUNT))
        buffer.write(BYTES_CATALOG.pack(U32, self.validatorIndex))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(deposit_stake_account)]: DON'T MODIFY
def deposit_stake_account(
    validator_list: Union[str, PublicKey, AccountMeta],
    stake_list: Union[str, PublicKey, AccountMeta],
    stake_account: Union[str, PublicKey, AccountMeta],
    duplication_flag: Union[str, PublicKey, AccountMeta],
    rent_payer: Union[str, PublicKey, AccountMeta],
    mint_to: Union[str, PublicKey, AccountMeta],
    stake_program: Union[str, PublicKey, AccountMeta],
    validatorIndex: U32,
    state: Union[str, PublicKey, AccountMeta] = STATE,
    stake_authority: Union[str, PublicKey, AccountMeta] = STAKE_AUTHORITY,
    msol_mint: Union[str, PublicKey, AccountMeta] = MSOL_MINT,
    msol_mint_authority: Union[str, PublicKey, AccountMeta] = MSOL_MINT_AUTHORITY,
    clock: Union[str, PublicKey, AccountMeta] = CLOCK,
    rent: Union[str, PublicKey, AccountMeta] = RENT,
    system_program: Union[str, PublicKey, AccountMeta] = SYSTEM_PROGRAM,
    token_program: Union[str, PublicKey, AccountMeta] = TOKEN_PROGRAM,
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
    if isinstance(validator_list, (str, PublicKey)):
        validator_list = to_account_meta(
            validator_list,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(stake_list, (str, PublicKey)):
        stake_list = to_account_meta(
            stake_list,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(stake_account, (str, PublicKey)):
        stake_account = to_account_meta(
            stake_account,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(stake_authority, (str, PublicKey)):
        stake_authority = to_account_meta(
            stake_authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(duplication_flag, (str, PublicKey)):
        duplication_flag = to_account_meta(
            duplication_flag,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(rent_payer, (str, PublicKey)):
        rent_payer = to_account_meta(
            rent_payer,
            is_signer=True,
            is_writable=True,
        )
    if isinstance(msol_mint, (str, PublicKey)):
        msol_mint = to_account_meta(
            msol_mint,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(mint_to, (str, PublicKey)):
        mint_to = to_account_meta(
            mint_to,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(msol_mint_authority, (str, PublicKey)):
        msol_mint_authority = to_account_meta(
            msol_mint_authority,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(clock, (str, PublicKey)):
        clock = to_account_meta(
            clock,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(rent, (str, PublicKey)):
        rent = to_account_meta(
            rent,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(token_program, (str, PublicKey)):
        token_program = to_account_meta(
            token_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(stake_program, (str, PublicKey)):
        stake_program = to_account_meta(
            stake_program,
            is_signer=False,
            is_writable=False,
        )

    return DepositStakeAccountIx(
        program_id=program_id,
        state=state,
        validator_list=validator_list,
        stake_list=stake_list,
        stake_account=stake_account,
        stake_authority=stake_authority,
        duplication_flag=duplication_flag,
        rent_payer=rent_payer,
        msol_mint=msol_mint,
        mint_to=mint_to,
        msol_mint_authority=msol_mint_authority,
        clock=clock,
        rent=rent,
        system_program=system_program,
        token_program=token_program,
        stake_program=stake_program,
        remaining_accounts=remaining_accounts,
        validatorIndex=validatorIndex,
    ).to_instruction()

# LOCK-END
