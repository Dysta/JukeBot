from collections import abc
from typing import Generic, TypeVar

_T = TypeVar("_T")
_V = TypeVar("_V")


class AbstractCache(abc.MutableSequence, Generic[_T, _V]):
    _cache: dict = {}

    def __setitem__(self, k: _T, v: _V) -> None:
        self._cache[k] = v

    def __contains__(self, k: _T):
        try:
            self._cache[k]
        except KeyError:
            return False
        return True

    def __delitem__(self, k: _T) -> None:
        del self._cache[k]

    def __getitem__(self, k: _T) -> _V:
        return self._cache[k]

    def __len__(self) -> int:
        return len(self._cache)

    def __str__(self) -> str:
        return str(self._cache)

    def clear(self) -> None:
        self._cache = {}

    def insert(self, index: _T, value: _V) -> None:
        self.__setitem__(index, value)
