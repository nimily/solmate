# LOCK-BEGIN[imports]: DON'T MODIFY
from pod import (
    Enum,
    U64,
    pod,
)
from solmate.anchor import Discriminant
from codegen.idl.types.array_of_enum_with_fields import ArrayOfEnumWithFields
from codegen.idl.types.risk_output_register import RiskOutputRegister

# LOCK-END


# LOCK-BEGIN[accounts]: DON'T MODIFY
@pod
class Accounts(Enum[U64]):
    ARRAY_OF_ENUM_WITH_FIELDS = Discriminant(field=ArrayOfEnumWithFields)
    RISK_OUTPUT_REGISTER = Discriminant(field=RiskOutputRegister)
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
