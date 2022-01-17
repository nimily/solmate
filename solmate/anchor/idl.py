from itertools import chain
from typing import Optional, Tuple

from pod import pod_json, Vec, Enum, Variant, named_fields, Default, Delayed
from pod.types.enum import ENUM_TAG_NAME, ENUM_TAG_NAME_MAP
from pod.json import POD_OPTIONS_RENAME


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

    OPTION = Variant(field=Delayed["IdlType"])
    VEC = Variant(field=Delayed["IdlType"])
    ARRAY = Variant(field=Tuple[Delayed["IdlType"], int])


@pod_json
class IdlField:
    name: str
    type: IdlType


@pod_json
class EnumFields(Enum):
    NAMED = Variant(field=Vec[IdlField])
    TUPLE = Variant(field=Vec[IdlType])

    @classmethod
    def _from_json(cls, raw):
        assert isinstance(raw, list)
        if len(raw) == 0:
            return EnumFields.NAMED([])

        if "name" in raw[0]:
            field = Vec[IdlField].from_json(raw)
            return EnumFields.NAMED(field)
        else:
            field = Vec[IdlType].from_json(raw)
            return EnumFields.TUPLE(field)

    @classmethod
    def _to_json(cls, instance):
        raise NotImplementedError


@pod_json
class IdlEnumVariant:
    name: str
    fields: Default[Optional[EnumFields], lambda: None]


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
    fields: Default[Vec[IdlEventField], []]


@pod_json
class IdlErrorCode:
    code: int
    name: str
    msg: Default[Vec[IdlEventField], lambda: None]


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


@pod_json
class IdlAccounts:
    __enum_options__ = {ENUM_TAG_NAME_MAP: camel_case}

    name: str
    accounts: Vec[Delayed["IdlAccountItem"]]


@pod_json
class IdlAccountItem(Enum):  # here
    IDL_ACCOUNT = Variant(field=IdlAccount)
    IDL_ACCOUNTS = Variant(field=IdlAccounts)

    @classmethod
    def _from_json(cls, raw):
        assert isinstance(raw, dict)

        if "accounts" in raw:
            field = Vec[IdlAccounts].from_json(raw)
            return IdlAccountItem.IDL_ACCOUNTS(field)
        else:
            field = IdlAccount.from_json(raw)
            return IdlAccountItem.IDL_ACCOUNT(field)

    @classmethod
    def _to_json(cls, instance):
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
    constants: Default[Vec[IdlConst], list]
    instructions: Default[Vec[IdlInstruction], list]
    state: Default[Optional[IdlState], None]
    accounts: Default[Vec[IdlTypeDefinition], list]
    types: Default[Vec[IdlTypeDefinition], list]
    events: Default[Vec[IdlEvent], list]
    errors: Default[Vec[IdlErrorCode], list]
    metadata: Default[Optional[object], None]
