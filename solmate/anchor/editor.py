import os

from typing import List, Dict
from pathlib import Path

LOCK_HEADER = "# LOCK-BEGIN["
LOCK_FOOTER = "# LOCK-END"
LOCK_WARNING = "]: DON'T MODIFY"


class CodeEditor:
    _filepath: str
    _lines: List[str]
    _locks: Dict[str, slice]

    def __init__(self, filepath):
        self._filepath = filepath
        self._lines = []
        self._locks = {}

    @property
    def locks(self):
        return self._locks.copy()

    def _to_slice(self, key):
        if isinstance(key, str):
            key = self._locks[key]
        elif isinstance(key, int):
            key = slice(key, key + 1)
        elif not isinstance(key, slice):
            raise ValueError(f"Unknown key type {type(key)}")

        return key

    def __len__(self):
        return len(self._lines)

    def __str__(self):
        return f"CodeEditor({self._filepath})"

    def __repr__(self):
        return f'CodeEditor("{self._filepath}")'

    def __delitem__(self, key):
        self[key] = []

    def __getitem__(self, key):
        key = self._to_slice(key)

        return self._lines[key]

    def __setitem__(self, key, new_lines):
        if isinstance(key, str):
            name = key
            if name not in self._locks:
                key = slice(len(self), len(self))
        else:
            name = None

        key = self._to_slice(key)
        start = key.start if key.start is not None else 0
        stop = key.stop if key.stop is not None else len(self)

        contained = self._get_contained_locks(start, stop)
        for name, count in contained.items():
            if count == 1:
                raise ValueError(f"Lines {key} have intersection with lock {name}")

        for name in contained:
            del self._locks[name]

        if isinstance(new_lines, str):
            new_lines = [new_lines]

        self._lines = self._lines[:start] + new_lines + self._lines[stop:]
        self._shift_lock_boundaries(start, len(new_lines) - (stop - start))
        if name is not None:
            self.set_lock(name, start, start + len(new_lines), check=False)

    def _shift_lock_boundaries(self, origin, diff):
        locks = {}
        for name, lock in self._locks.items():
            start = lock.start
            stop = lock.stop

            if start > origin:
                start += diff

            if stop > origin:
                stop += diff

            if start < stop:
                locks[name] = slice(start, stop)

        self._locks = locks

    def _get_contained_locks(self, start, stop):
        if start == stop:
            return {}

        counts = {}
        for name, lock in self._locks.items():
            if start == lock.start or stop == lock.stop:
                if start < lock.start or lock.stop < stop:
                    counts[name] = 2
            else:
                include_start = (start <= lock.start) and (lock.start < stop)
                include_end = (start < lock.stop) and (lock.stop <= stop)
                n_overlaps = include_start + include_end

                if n_overlaps > 0:
                    counts[name] = n_overlaps

        return counts

    def add_lines(self, *lines, lineno=None):
        if lineno is None:
            lineno = len(self)

        self[lineno:lineno] = list(lines)

    def set_lock(self, name, start, stop, check=True):
        if check:
            for lock in self._locks.values():
                # checking if new lock has intersection with an existing one
                if max(start, lock.start) <= min(stop, lock.stop):
                    raise RuntimeError(
                        "Failed to set the lock due to non-empty intersection with existing lock."
                    )
        self._locks[name] = slice(start, stop)

    @staticmethod
    def _get_indent(line: str):
        n_blanks = len(line) - len(line.lstrip())

        return line[:n_blanks]

    @staticmethod
    def wrap_with_lock(name, lines, header_indent=None, footer_indent=None):
        if header_indent is None:
            if lines:
                header_indent = CodeEditor._get_indent(lines[0])
            else:
                header_indent = ""

        if footer_indent is None:
            if lines:
                footer_indent = CodeEditor._get_indent(lines[-1])
            else:
                footer_indent = ""

        header = header_indent + LOCK_HEADER + name + LOCK_WARNING + "\n"
        footer = footer_indent + LOCK_FOOTER + "\n"

        return [header] + lines + [footer]

    def get_source_code(self):
        return "".join(self._lines)

    def infer_locks(self):
        locks = {}
        name = None
        start = None
        for lineno, line in enumerate(self._lines):
            stripped = line.strip()
            if stripped.startswith(LOCK_HEADER):
                if start is not None:
                    raise RuntimeError("Nested locks are not supported.")

                if not stripped.endswith(LOCK_WARNING):
                    raise RuntimeError("Malformed lock header")

                start = lineno
                name = stripped[len(LOCK_HEADER) : -len(LOCK_WARNING)]
            elif stripped == LOCK_FOOTER:
                locks[name] = slice(start, lineno + 1)
                name = None
                start = None

        if start is not None:
            raise RuntimeError(f"Lock '{name}' never ended.")

        self._locks = locks

    def load(self, infer=True):
        if not os.path.exists(self._filepath):
            return

        with open(self._filepath, "r") as file:
            self._lines = file.readlines()

        if infer:
            self.infer_locks()

    def save(self):
        path = Path(self._filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as file:
            file.write(self.get_source_code())


def cli():
    ce = CodeEditor("/Users/nimily/Workspaces/python/solmate/solmate/anchor/test.py")
    ce.load()
    ce["taghi"] = []
    ce["bbb"] = []
    # ce["aaa"] = []
    # del ce["taghi"]
    ce.add_lines("hello\n", "bye\n")
    print("nima" in ce.locks)
    ce["nima"] = ["test\n", "success\n"]
    ce["nima"] = ce.wrap_with_lock("nima", ["line a\n", "line b\n"])
    print(ce.get_source_code())
    print(ce.locks)
    print("nima" in ce.locks)
    # ce.save()
    # print(ce[5:7])
    # print("".join(ce._lines[ce._locks["bbb"]]))
