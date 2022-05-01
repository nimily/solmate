import json
from itertools import chain
from typing import Optional, Tuple  # pylint: disable=unused-import

from podite import pod_json, field, named_fields, Vec, Enum, Variant
from podite.types.enum import ENUM_TAG_NAME, ENUM_TAG_NAME_MAP
from podite.json import POD_OPTIONS_RENAME

from solmate.utils import camel_to_snake


def camel_case(name):
    head, *tail = name.split("_")
    return "".join(chain([head.lower()], map(str.capitalize, tail)))


@pod_json
class IdlType(Enum):
    __enum_options__ = {ENUM_TAG_NAME_MAP: camel_case}

    BOOL = None
    U8 = None
    I8 = None
    U16 = None
    I16 = None
    U32 = None
    I32 = None
    U64 = None
    I64 = None
    U128 = None
    I128 = None
    BYTES = None
    STRING = None
    PUBLIC_KEY = None
    DEFINED = Variant(field=str)

    OPTION = Variant(field="IdlType")
    COPTION = Variant(field="IdlType")
    STATIC = Variant(field="IdlType")
    VEC = Variant(field="IdlType")
    ARRAY = Variant(field="Tuple[IdlType, int]")


@pod_json
class IdlField:
    name: str
    type: IdlType

    @property
    def py_name(self):
        return camel_to_snake(self.name)


@pod_json
class EnumFields(Enum):
    NAMED = Variant(field=Vec[IdlField])
    TUPLE = Variant(field=Vec[IdlType])

    @classmethod
    def _from_dict(cls, raw):
        assert isinstance(raw, list)
        if len(raw) == 0:
            return EnumFields.NAMED([])

        if "name" in raw[0]:
            field_val = Vec[IdlField].from_dict(raw)
            return EnumFields.NAMED(field_val)
        else:
            field_val = Vec[IdlType].from_dict(raw)
            return EnumFields.TUPLE(field_val)

    @classmethod
    def _to_dict(cls, instance):
        raise NotImplementedError


@pod_json
class IdlEnumVariant:
    name: str
    fields: Optional[EnumFields] = field(default=None)


@pod_json
class IdlTypeDefinitionTy(Enum):
    __enum_options__ = {
        ENUM_TAG_NAME: "kind",
        ENUM_TAG_NAME_MAP: "lower",
    }

    STRUCT = Variant(field=named_fields(fields=Vec[IdlField]))
    ENUM = Variant(field=named_fields(variants=Vec[IdlEnumVariant]))


@pod_json
class IdlTypeDefinition:
    name: str
    type: IdlTypeDefinitionTy


@pod_json
class IdlEventField:
    name: str
    type: IdlType
    index: bool


@pod_json
class IdlEvent:
    name: str
    fields: Vec[IdlEventField] = field(default_factory=list)


@pod_json
class IdlErrorCode:
    code: int
    name: str
    msg: Optional[str] = field(default=None)


@pod_json
class IdlConst:
    name: str
    type: IdlType
    value: str


@pod_json
class IdlAccount:
    __pod_options__ = {POD_OPTIONS_RENAME: camel_case}

    name: str
    is_mut: bool
    is_signer: bool
    is_optional: bool = field(default=False)


@pod_json
class IdlAccounts:
    __enum_options__ = {ENUM_TAG_NAME_MAP: camel_case}

    name: str
    accounts: Vec["IdlAccountItem"]


@pod_json
class IdlAccountItem(Enum):
    IDL_ACCOUNT = Variant(field=IdlAccount)
    IDL_ACCOUNTS = Variant(field=IdlAccounts)

    @classmethod
    def _from_dict(cls, raw):
        assert isinstance(raw, dict)

        if "accounts" in raw:
            name = raw["name"]
            sub_accounts = Vec[IdlAccountItem].from_dict(raw["accounts"])
            field_value = IdlAccounts(name, sub_accounts)
            return IdlAccountItem.IDL_ACCOUNTS(field_value)
        else:
            field_value = IdlAccount.from_dict(raw)
            return IdlAccountItem.IDL_ACCOUNT(field_value)

    @classmethod
    def _to_dict(cls, instance):
        raise NotImplementedError


@pod_json
class IdlInstruction:
    name: str
    accounts: Vec[IdlAccountItem]
    args: Vec[IdlField]


@pod_json
class IdlState:
    struct: IdlTypeDefinition
    methods: Vec[IdlInstruction]


@pod_json
class Idl:
    version: str
    name: str
    constants: Vec[IdlConst] = field(default_factory=list)
    instructions: Vec[IdlInstruction] = field(default_factory=list)
    state: Optional[IdlState] = field(default=None)
    accounts: Vec[IdlTypeDefinition] = field(default_factory=list)
    types: Vec[IdlTypeDefinition] = field(default_factory=list)
    events: Vec[IdlEvent] = field(default_factory=list)
    errors: Vec[IdlErrorCode] = field(default_factory=list)
    metadata: Optional[object] = field(default=None)

    @staticmethod
    def from_json_file(filename):
        with open(filename, "r") as fin:
            idl_dict = json.load(fin)
            return Idl.from_dict(idl_dict)
