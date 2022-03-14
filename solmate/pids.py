from solana.publickey import PublicKey

_PIDS = dict()


def get_pids_or_default(protocol_name: str, default: PublicKey):
    global _PIDS
    return _PIDS.get(key=protocol_name, default=default)


def set_pid_by_protocol_name(protocol_name: str, pid: PublicKey):
    global _PIDS
    _PIDS[protocol_name] = pid