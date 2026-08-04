from __future__ import annotations

from collections import abc
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TypeVar

_T = TypeVar("_T")


@dataclass
class AbstractCollection[T](abc.Collection):
    set: list[_T]

    def __len__(self) -> int:
        return len(self.set)

    def __iter__(self) -> Iterator[_T]:
        yield from self.set

    def __contains__(self, e: object) -> bool:
        return e in self.set

    def __getitem__(self, idx: int) -> _T:
        return self.set[idx]

    def __str__(self) -> str:
        return str(self.set)

    def __add__(self, other: AbstractCollection) -> AbstractCollection:
        assert isinstance(other, AbstractCollection)
        self.set += other.set
        return self
