# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Enum,
    U8,
    Variant,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(AuthorityType)]: DON'T MODIFY
@pod
class AuthorityType(Enum[U8]):
    MINT_TOKENS = Variant(0)
    FREEZE_ACCOUNT = Variant(1)
    ACCOUNT_OWNER = Variant(2)
    CLOSE_ACCOUNT = Variant(3)
    # LOCK-END

    @classmethod
    def _to_bytes_partial(cls, buffer, obj, **kwargs):
        # to modify packing, change this method
        return super()._to_bytes_partial(buffer, obj, **kwargs)

    @classmethod
    def _from_bytes_partial(cls, buffer, **kwargs):
        # to modify unpacking, change this method
        return super()._from_bytes_partial(buffer, **kwargs)

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
