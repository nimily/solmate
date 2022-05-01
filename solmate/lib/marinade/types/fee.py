# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    U32,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(Fee)]: DON'T MODIFY
@pod
class Fee:
    basis_points: U32
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
