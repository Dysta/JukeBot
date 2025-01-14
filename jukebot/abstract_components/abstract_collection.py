from __future__ import annotations

from collections import abc
from dataclasses import dataclass
from typing import Generic, Iterator, List, TypeVar

_T = TypeVar("_T")


@dataclass
class AbstractCollection(abc.Collection, Generic[_T]):
    set: List[_T]

    def __len__(self) -> int:
        return len(self.set)

    def __iter__(self) -> Iterator[_T]:
        for e in self.set:
            yield e

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
