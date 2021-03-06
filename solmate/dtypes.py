from io import BytesIO
from typing import Type

from podite import U32, U64, I64, Enum, Variant, Option, pod, BYTES_CATALOG
from podite._utils import _GetitemToCall, get_calling_module, get_concrete_type

Usize = U64  # Should it be U32?
UnixTimestamp = I64


class Error(Variant):
    msg: str

    def __init__(self, /, value=None, field=None, module=None, msg=None):
        super().__init__(value, field, module)

        self.msg = msg

    def to_string(self, instance):
        msg = self.msg.format(instance.field)
        return f"{self.name}: {msg}"


class ProgramError(Enum):
    CUSTOM = Error(field=U32, msg="Custom program error: {}")
    INVALID_ARGUMENT = Error(
        msg="The arguments provided to a program instruction where invalid"
    )
    INVALID_INSTRUCTION_DATA = Error(msg="An instruction's data contents was invalid")
    INVALID_ACCOUNT_DATA = Error(msg="An account's data contents was invalid")
    ACCOUNT_DATA_TOO_SMALL = Error(msg="An account's data was too small")
    INSUFFICIENT_FUNDS = Error(
        msg="An account's balance was too small to complete the instruction"
    )
    INCORRECT_PROGRAM_ID = Error(msg="The account did not have the expected program id")
    MISSING_REQUIRED_SIGNATURE = Error(msg="A signature was required but not found")
    ACCOUNT_ALREADY_INITIALIZED = Error(
        msg="An initialize instruction was sent to an account that has already been initialized"
    )
    UNINITIALIZED_ACCOUNT = Error(
        msg="An attempt to operate on an account that hasn't been initialized"
    )
    NOT_ENOUGH_ACCOUNT_KEYS = Error(
        msg="The instruction expected additional account keys"
    )
    ACCOUNT_BORROW_FAILED = Error(msg="Failed to borrow a reference to account data")
    MAX_SEED_LENGTH_EXCEED = Error(
        msg="Length of the seed is too long for address generation"
    )
    INVALID_SEEDS = Error(msg="Provided seeds do not result in a valid address")
    BORCH_IO_ERROR = Error(field=str, msg="IO Error: {}")
    ACCOUNT_NOT_RENT_EXEMPT = Error(
        msg="An account does not have enough lamports to be rent-exempt"
    )
    UNSUPPORTED_SYSVAR = Error(msg="Unsupported sysvar")
    ILLEGAL_OWNER = Error(msg="Provided owner is not allowed")
    ACCOUNTS_DATA_BUDGET_EXCEEDED = Error(
        msg="Requested account data allocation exceeded the accounts data budget"
    )

    def __str__(self):
        variant = self._get_variant(self.get_name())
        return variant.to_string(self)


def _coption(name, type_: Type):
    @pod
    class _COption(Enum[U32]):
        NONE = Variant()
        SOME = Variant(field=type_, module=get_calling_module(4))

    _COption.__name__ = f"{name}[{type_}]"
    _COption.__qualname__ = _COption.__name__

    return _COption


COption = _GetitemToCall("COption", _coption)


def _coptional(name, type_: Type):
    module = get_calling_module()

    @pod
    class _COptional(Enum[U32]):
        @classmethod
        def _is_static(cls) -> bool:
            return False

        @classmethod
        def _calc_max_size(cls):
            return 4 + BYTES_CATALOG.calc_max_size(get_concrete_type(module, type_))

        @classmethod
        def _from_bytes_partial(cls, buffer, **kwargs):
            has_value = BYTES_CATALOG.unpack_partial(U32, buffer)
            if has_value:
                return BYTES_CATALOG.unpack_partial(
                    get_concrete_type(module, type_), buffer
                )
            else:
                return None

        @classmethod
        def _to_bytes_partial(cls, buffer, obj, **kwargs):
            if obj is None:
                BYTES_CATALOG.pack_partial(U32, buffer, 0)
            else:
                BYTES_CATALOG.pack_partial(U32, buffer, 1)
                BYTES_CATALOG.pack_partial(
                    get_concrete_type(module, type_), buffer, obj
                )

    _COptional.__name__ = f"{name}[{type_}]"
    _COptional.__qualname__ = _COptional.__name__

    return _COptional


COptional = _GetitemToCall("COptional", _coptional)


class Repeat:
    def __class_getitem__(
        cls, type_: Type, max_len=0, allow_remainder=False, ring=True
    ):
        module = get_calling_module()

        @pod(dataclass_fn=None)
        class _Repeat:
            payload: bytes
            elem_size: int

            @classmethod
            def _is_static(cls) -> bool:
                return False

            @classmethod
            def _calc_max_size(cls):
                if max_len == 0:
                    return 2 ** 32
                return (
                    BYTES_CATALOG.calc_max_size(get_concrete_type(module, type_))
                    * max_len
                )

            @classmethod
            def _from_bytes_partial(cls, buffer, **kwargs):
                obj = _Repeat()
                obj.payload = buffer.read()
                obj.elem_size = BYTES_CATALOG.calc_max_size(
                    get_concrete_type(module, type_)
                )

                if not allow_remainder and len(obj.payload) % obj.elem_size != 0:
                    raise RuntimeError(
                        "Remainder is not allowed but payload has remainder"
                    )

                if max_len > 0 and max_len * obj.elem_size > len(obj.payload):
                    raise RuntimeError(
                        f"Repeat cannot have more than {max_len} elements"
                    )

                return obj

            @classmethod
            def _to_bytes_partial(cls, buffer, obj, **kwargs):
                raise NotImplementedError()

            @property
            def n_elem(self):
                return len(self.payload) // self.elem_size

            def __getitem__(self, item):
                n_elem = self.n_elem
                if not ring:
                    if item < 0 or item >= n_elem:
                        raise ValueError(
                            f"Can only look up items in the range 0..{n_elem}"
                        )
                else:
                    item = item % n_elem

                start = item * self.elem_size
                end = (item + 1) * self.elem_size
                buffer = BytesIO(self.payload[start:end])

                return BYTES_CATALOG.unpack_partial(
                    get_concrete_type(module, type_), buffer
                )

        _Repeat.__name__ = f"Repeat[{type_}]"
        _Repeat.__qualname__ = _Repeat.__name__

        return _Repeat
