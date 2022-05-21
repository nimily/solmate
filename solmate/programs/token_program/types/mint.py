# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Static,
    U64,
    U8,
    pod,
)
from solana.publickey import PublicKey
from solmate.dtypes import COptional

# LOCK-END


# LOCK-BEGIN[class(Mint)]: DON'T MODIFY
@pod
class Mint:
    mint_authority: Static[COptional[PublicKey]]
    supply: U64
    decimals: U8
    is_initialized: bool
    freeze_authority: Static[COptional[PublicKey]]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
