# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    FixedLenArray,
    U8,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(Multisig)]: DON'T MODIFY
@pod
class Multisig:
    m: U8
    n: U8
    is_initialized: bool
    signers: FixedLenArray[PublicKey, 2]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
