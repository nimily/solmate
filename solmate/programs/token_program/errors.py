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
    NOT_RENT_EXEMPT = Variant(0, field="Lamport balance below rent-exempt threshold")
    INSUFFICIENT_FUNDS = Variant(1, field="Insufficient funds")
    INVALID_MINT = Variant(2, field="Invalid Mint")
    MINT_MISMATCH = Variant(3, field="Account not associated with this Mint")
    OWNER_MISMATCH = Variant(4, field="Owner does not match")
    FIXED_SUPPLY = Variant(5, field="Fixed supply")
    ALREADY_IN_USE = Variant(6, field="Already in use")
    INVALID_NUMBER_OF_PROVIDED_SIGNERS = Variant(
        7, field="Invalid number of provided signers"
    )
    INVALID_NUMBER_OF_REQUIRED_SIGNERS = Variant(
        8, field="Invalid number of required signers"
    )
    UNINITIALIZED_STATE = Variant(9, field="State is unititialized")
    NATIVE_NOT_SUPPORTED = Variant(
        10, field="Instruction does not support native tokens"
    )
    NON_NATIVE_HAS_BALANCE = Variant(
        11, field="Non-native account can only be closed if its balance is zero"
    )
    INVALID_INSTRUCTION = Variant(12, field="Invalid instruction")
    INVALID_STATE = Variant(13, field="State is invalid for requested operation")
    OVERFLOW = Variant(14, field="Operation overflowed")
    AUTHORITY_TYPE_NOT_SUPPORTED = Variant(
        15, field="Account does not support specified authority type"
    )
    MINT_CANNOT_FREEZE = Variant(16, field="This token mint cannot freeze accounts")
    ACCOUNT_FROZEN = Variant(17, field="Account is frozen")
    MINT_DECIMALS_MISMATCH = Variant(
        18, field="The provided decimals value different from the Mint decimals"
    )
    NON_NATIVE_NOT_SUPPORTED = Variant(
        19, field="Instruction does not support non-native tokens"
    )
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
