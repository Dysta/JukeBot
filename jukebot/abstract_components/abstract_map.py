from __future__ import annotations

from collections import abc
from typing import Generic, Iterator, TypeVar

_T = TypeVar("_T")
_V = TypeVar("_V")


class AbstractMap(abc.MutableMapping, Generic[_T, _V]):
    def __new__(cls):
        instance = super(AbstractMap, cls).__new__(cls)
        instance._collection = dict()
        return instance

    def __setitem__(self, k: _T, v: _V) -> None:
        self._collection[k] = v

    def __contains__(self, k: _T):
        return k in self._collection.keys()

    def __delitem__(self, k: _T) -> None:
        del self._collection[k]

    def __getitem__(self, k: _T) -> _V:
        return self._collection[k]

    def __len__(self) -> int:
        return len(self._collection)

    def __iter__(self) -> Iterator[_T]:
        for e in self._collection:
            yield e

    def __str__(self) -> str:
        return str(self._collection)
