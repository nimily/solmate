from solana.publickey import PublicKey
from typing import Dict

_PIDS: Dict[str, PublicKey] = dict()


def get_pid_or_default(protocol_name: str, default: PublicKey):
    global _PIDS
    return _PIDS.get(protocol_name, default)


def set_pid_by_protocol_name(protocol_name: str, pid: PublicKey):
    global _PIDS
    _PIDS[protocol_name] = pid
