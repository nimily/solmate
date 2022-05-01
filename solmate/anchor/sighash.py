from hashlib import sha256

from podite import U64


def sighash(namespace: str, name: str) -> int:
    preimage = f"{namespace}:{name}".encode()
    hash_bytes = sha256(preimage).digest()

    return U64.from_bytes(hash_bytes[:8])
