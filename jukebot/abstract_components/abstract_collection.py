from collections import abc
from typing import Iterator, TypeVar, Generic

_T = TypeVar("_T")
_V = TypeVar("_V")


class AbstractCollection(abc.MutableMapping, Generic[_T, _V]):
    def __setitem__(self, k: _T, v: _V) -> None:
        self.__dict__[k] = v

    def __contains__(self, k: _T):
        return k in self.__dict__.keys()

    def __delitem__(self, k: _T) -> None:
        del self.__dict__[k]

    def __getitem__(self, k: _T) -> _V:
        return self.__dict__[k]

    def __len__(self) -> int:
        return len(self.__dict__)

    def __iter__(self) -> Iterator[_T]:
        for e in self.__dict__:
            yield e

    def __str__(self) -> str:
        return str(self.__dict__)
