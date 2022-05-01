from typing import Type

from podite import U32, U64, I64, Enum, Variant, Option, pod
from podite._utils import _GetitemToCall, get_calling_module


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
