from collections import abc
from dataclasses import dataclass
from typing import TypeVar, List, Generic, Iterator

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
        if 0 <= idx < len(self):
            return self.set[idx]
        raise IndexError
