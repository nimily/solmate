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
    WRONG_RESERVE_OWNER = Variant(6000, field="Wrong reserve owner. Must be a system account")
    NON_EMPTY_RESERVE_DATA = Variant(6001, field="Reserve must have no data, but has data")
    INVALID_INITIAL_RESERVE_LAMPORTS = Variant(6002, field="Invalid initial reserve lamports")
    ZERO_VALIDATOR_CHUNK_SIZE = Variant(6003, field="Zero validator chunk size")
    TOO_BIG_VALIDATOR_CHUNK_SIZE = Variant(6004, field="Too big validator chunk size")
    ZERO_CREDIT_CHUNK_SIZE = Variant(6005, field="Zero credit chunk size")
    TOO_BIG_CREDIT_CHUNK_SIZE = Variant(6006, field="Too big credit chunk size")
    TOO_LOW_CREDIT_FEE = Variant(6007, field="Too low credit fee")
    INVALID_MINT_AUTHORITY = Variant(6008, field="Invalid mint authority")
    MINT_HAS_INITIAL_SUPPLY = Variant(6009, field="Non empty initial mint supply")
    INVALID_OWNER_FEE_STATE = Variant(6010, field="Invalid owner fee state")
    INVALID_PROGRAM_ID = Variant(12116, field="1910 Invalid program id. For using program from another account please update id in the code")
    UNEXPECTED_ACCOUNT = Variant(71140, field="FFA0 Unexpected account")
    CALCULATION_FAILURE = Variant(57619, field="CACF Calculation failure")
    ACCOUNT_WITH_LOCKUP = Variant(51694, field="B3AA You can't deposit a stake-account with lockup")
    NUMBER_TOO_LOW = Variant(13892, field="2000 Number too low")
    NUMBER_TOO_HIGH = Variant(13893, field="2001 Number too high")
    FEE_TOO_HIGH = Variant(10052, field="1100 Fee too high")
    FEES_WRONG_WAY_ROUND = Variant(10053, field="1101 Min fee > max fee")
    LIQUIDITY_TARGET_TOO_LOW = Variant(10054, field="1102 Liquidity target too low")
    TICKET_NOT_DUE = Variant(10055, field="1103 Ticket not due. Wait more epochs")
    TICKET_NOT_READY = Variant(10056, field="1104 Ticket not ready. Wait a few hours and try again")
    WRONG_BENEFICIARY = Variant(10057, field="1105 Wrong Ticket Beneficiary")
    INSUFFICIENT_LIQUIDITY = Variant(10205, field="1199 Insufficient Liquidity in the Liquidity Pool")
    INVALID_VALIDATOR = Variant(53525, field="BAD1 Invalid validator")
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
