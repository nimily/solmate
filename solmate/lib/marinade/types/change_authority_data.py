# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Option,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(ChangeAuthorityData)]: DON'T MODIFY
@pod
class ChangeAuthorityData:
    admin: Option[PublicKey]
    validator_manager: Option[PublicKey]
    operational_sol_account: Option[PublicKey]
    treasury_msol_account: Option[PublicKey]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
