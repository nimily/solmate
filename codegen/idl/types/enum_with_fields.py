# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    AutoTagType,
    Enum,
    Variant,
    pod,
)
from codegen.idl.types.call_back_info import CallBackInfo
from codegen.idl.types.action_status import ActionStatus

# LOCK-END


# LOCK-BEGIN[class(EnumWithFields)]: DON'T MODIFY
@pod
class EnumWithFields(Enum[AutoTagType]):
    HEALTH = Variant(field=CallBackInfo)
    LIQUIDATION = Variant(field=ActionStatus)
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
