# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    FixedLenArray,
    pod,
)
from codegen.idl.types.enum_with_fields import EnumWithFields

# LOCK-END


# LOCK-BEGIN[class(ArrayOfEnumWithFields)]: DON'T MODIFY
@pod
class ArrayOfEnumWithFields:
    array: FixedLenArray[EnumWithFields, 256]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
