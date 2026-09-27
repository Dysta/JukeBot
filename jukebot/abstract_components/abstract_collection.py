from __future__ import annotations

from collections import abc
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass
class AbstractCollection[T](abc.Collection):
    set: list[T]

    def __len__(self) -> int:
        return len(self.set)

    def __iter__(self) -> Iterator[T]:
        yield from self.set

    def __contains__(self, e: object) -> bool:
        return e in self.set

    def __getitem__(self, idx: int) -> T:
        return self.set[idx]

    def __str__(self) -> str:
        return str(self.set)

    def __add__(self, other: AbstractCollection) -> AbstractCollection:
        assert isinstance(other, AbstractCollection)
        self.set += other.set
        return self
