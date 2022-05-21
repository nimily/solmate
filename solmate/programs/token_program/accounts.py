# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    BYTES_CATALOG,
    Enum,
    U8,
    Variant,
    pod,
)
from solmate.programs.token_program.types.account import Account
from solmate.programs.token_program.types.mint import Mint
from solmate.programs.token_program.types.multisig import Multisig

# LOCK-END


# LOCK-BEGIN[accounts]: DON'T MODIFY
@pod
class Accounts(Enum[U8]):
    MINT = Variant(field=Mint)
    ACCOUNT = Variant(field=Account)
    MULTISIG = Variant(field=Multisig)

    @classmethod
    def _from_bytes_partial(cls, buffer, **kwargs):
        account_len = buffer.getbuffer().nbytes - buffer.tell()
        if account_len == Mint.calc_max_size():
            obj = BYTES_CATALOG.unpack_partial(Mint, buffer)
            return Accounts.MINT(obj)

        if account_len == Account.calc_max_size():
            obj = BYTES_CATALOG.unpack_partial(Account, buffer)
            return Accounts.ACCOUNT(obj)

        if account_len == Multisig.calc_max_size():
            obj = BYTES_CATALOG.unpack_partial(Multisig, buffer)
            return Accounts.MULTISIG(obj)

    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
