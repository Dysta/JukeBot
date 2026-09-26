from __future__ import annotations

from collections import abc
from collections.abc import Iterator


class AbstractMap[T, V](abc.MutableMapping):
    _collection: dict[T, V]

    def __new__(cls):
        instance = super().__new__(cls)
        instance._collection = {}
        return instance

    def __setitem__(self, k: T, v: V) -> None:
        self._collection[k] = v

    def __contains__(self, k: object) -> bool:
        return k in self._collection

    def __delitem__(self, k: T) -> None:
        del self._collection[k]

    def __getitem__(self, k: T) -> V:
        return self._collection[k]

    def __len__(self) -> int:
        return len(self._collection)

    def __iter__(self) -> Iterator[T]:
        yield from self._collection

    def __str__(self) -> str:
        return str(self._collection)
