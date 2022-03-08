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
from io import BytesIO
from .instruction_tag import InstructionTag
from solmate.lib.marinade.addrs import (
    MAIN_STATE as STATE,
    PROGRAM_ID,
    RESERVE_PDA,
)
from solana.sysvar import SYSVAR_CLOCK_PUBKEY as CLOCK
from solmate.lib.system_program import PROGRAM_ID as SYSTEM_PROGRAM
from solmate.utils import to_account_meta

# LOCK-END


# LOCK-BEGIN[ix_cls(claim)]: DON'T MODIFY
@dataclass
class ClaimIx:
    program_id: PublicKey

    # account metas
    state: AccountMeta
    reserve_pda: AccountMeta
    ticket_account: AccountMeta
    transfer_sol_to: AccountMeta
    clock: AccountMeta
    system_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.state)
        keys.append(self.reserve_pda)
        keys.append(self.ticket_account)
        keys.append(self.transfer_sol_to)
        keys.append(self.clock)
        keys.append(self.system_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.CLAIM))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(claim)]: DON'T MODIFY
def claim(
    ticket_account: Union[str, PublicKey, AccountMeta],
    transfer_sol_to: Union[str, PublicKey, AccountMeta],
    state: Union[str, PublicKey, AccountMeta] = STATE,
    reserve_pda: Union[str, PublicKey, AccountMeta] = RESERVE_PDA,
    clock: Union[str, PublicKey, AccountMeta] = CLOCK,
    system_program: Union[str, PublicKey, AccountMeta] = SYSTEM_PROGRAM,
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
    if isinstance(reserve_pda, (str, PublicKey)):
        reserve_pda = to_account_meta(
            reserve_pda,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(ticket_account, (str, PublicKey)):
        ticket_account = to_account_meta(
            ticket_account,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(transfer_sol_to, (str, PublicKey)):
        transfer_sol_to = to_account_meta(
            transfer_sol_to,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(clock, (str, PublicKey)):
        clock = to_account_meta(
            clock,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )

    return ClaimIx(
        program_id=program_id,
        state=state,
        reserve_pda=reserve_pda,
        ticket_account=ticket_account,
        transfer_sol_to=transfer_sol_to,
        clock=clock,
        system_program=system_program,
        remaining_accounts=remaining_accounts,
    ).to_instruction()

# LOCK-END
