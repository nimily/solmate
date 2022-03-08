# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    Enum,
    U64,
    pod,
)
from solmate.anchor import AccountDiscriminant
from solmate.lib.marinade.types.state import State
from solmate.lib.marinade.types.ticket_account_data import TicketAccountData

# LOCK-END


# LOCK-BEGIN[accounts]: DON'T MODIFY
@pod
class Accounts(Enum[U64]):
    STATE = AccountDiscriminant(field=State)
    TICKET_ACCOUNT_DATA = AccountDiscriminant(field=TicketAccountData)
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
