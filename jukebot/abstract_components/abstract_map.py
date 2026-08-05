from __future__ import annotations

from collections import abc
from collections.abc import Iterator
from typing import TypeVar

_T = TypeVar("_T")
_V = TypeVar("_V")


class AbstractMap[T, V](abc.MutableMapping):
    def __new__(cls):
        instance = super().__new__(cls)
        instance._collection = {}
        return instance

    def __setitem__(self, k: _T, v: _V) -> None:
        self._collection[k] = v

    def __contains__(self, k: _T):
        return k in self._collection

    def __delitem__(self, k: _T) -> None:
        del self._collection[k]

    def __getitem__(self, k: _T) -> _V:
        return self._collection[k]

    def __len__(self) -> int:
        return len(self._collection)

    def __iter__(self) -> Iterator[_T]:
        yield from self._collection

    def __str__(self) -> str:
        return str(self._collection)
