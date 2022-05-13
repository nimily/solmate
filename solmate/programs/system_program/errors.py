# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    Enum,
    U64,
    Variant,
    pod,
)

# LOCK-END


# LOCK-BEGIN[errors]: DON'T MODIFY
@pod
class Error(Enum[U64]):
    ACCOUNT_ALREADY_IN_USE = Variant(
        0, field="An account with the same address already exists"
    )
    RESULT_WITH_NEGATIVE_LAMPORTS = Variant(
        1, field="Account does not have enough SOL to perform the operation"
    )
    INVALID_PROGRAM_ID = Variant(2, field="Cannot assign account to this program id")
    INVALID_ACCOUNT_DATA_LENGTH = Variant(
        3, field="Cannot allocate account data of this length"
    )
    MAX_SEED_LENGTH_EXCEEDED = Variant(4, field="Length of requested seed is too long")
    ADDRESS_WITH_SEED_MISMATCH = Variant(
        5, field="Provided address does not match addressed derived from seed"
    )
    NONCE_NO_RECENT_BLOCKHASHES = Variant(
        6, field="Advancing stored nonce requires a populated RecentBlockhashes sysvar"
    )
    NONCE_BLOCKHASH_NOT_EXPIRED = Variant(
        7, field="Stored nonce is still in recent_blockhashes"
    )
    NONCE_UNEXPECTED_BLOCKHASH_VALUE = Variant(
        8, field="Specified nonce does not match stored nonce"
    )
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
