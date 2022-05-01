__version__ = "0.1.0"

from typing import Any

from podite import get_catalog
from podite.bytes import BytesPodConverter
from podite.json import JsonPodConverter
from solana.publickey import PublicKey


def register_solana_types_converters():
    class SolanaTypesPodConverter(BytesPodConverter, JsonPodConverter):
        def get_mapping(self, type_):
            if type_ in (PublicKey,):
                return self

            return None

        def is_static(self, type_) -> bool:
            if type_ == PublicKey:
                return True

            raise ValueError()

        def calc_size(self, type_, obj, **kwargs) -> int:
            if type_ == PublicKey:
                return 32

            raise ValueError()

        def calc_max_size(self, type_) -> int:
            if type_ == PublicKey:
                return 32

            raise ValueError()

        def pack_partial(self, type_, buffer, obj, **kwargs) -> Any:
            if type_ == PublicKey:
                return buffer.write(bytes(obj))

            raise ValueError()

        def unpack_partial(self, type_, buffer, **kwargs) -> Any:
            if type_ == PublicKey:
                return PublicKey(buffer.read(32))

            raise ValueError()

        def pack_dict(self, type_, obj, **kwargs) -> Any:
            if type_ == PublicKey:
                return str(obj)

            raise ValueError()

        def unpack_dict(self, type_, obj, **kwargs) -> Any:
            if type_ == PublicKey:
                if not isinstance(obj, str):
                    raise ValueError("PublicKey has to be encoded as a string.")

                return PublicKey(obj)

            raise ValueError()

    converter = SolanaTypesPodConverter()
    get_catalog("bytes").register(converter.get_mapping)
    get_catalog("json").register(converter.get_mapping)


register_solana_types_converters()
