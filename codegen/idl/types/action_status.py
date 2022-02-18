# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    Enum,
    U8,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(ActionStatus)]: DON'T MODIFY
@pod
class ActionStatus(Enum[U8]):
    APPROVED = None
    NOT_APPROVED = None
    # LOCK-END

    @classmethod
    def _to_bytes_partial(cls, buffer, obj):
        # to modify packing, change this method
        return super()._to_bytes_partial(buffer, obj)

    @classmethod
    def _from_bytes_partial(cls, buffer):
        # to modify unpacking, change this method
        return super()._from_bytes_partial(buffer)

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
