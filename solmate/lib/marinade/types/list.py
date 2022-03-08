# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    U32,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(List)]: DON'T MODIFY
@pod
class List:
    account: PublicKey
    item_size: U32
    count: U32
    new_account: PublicKey
    copied_count: U32
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
