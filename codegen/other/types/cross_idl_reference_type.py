# LOCK-BEGIN[imports]: DON'T MODIFY
from codegen.idl.types.call_back_info import CallBackInfo
from pod import pod
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(CrossIdlReferenceType)]: DON'T MODIFY
@pod
class CrossIdlReferenceType:
    user_account: PublicKey
    call_back_info_field: CallBackInfo
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
