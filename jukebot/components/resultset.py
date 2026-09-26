from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from jukebot.abstract_components import AbstractCollection
from jukebot.components.result import Result

if TYPE_CHECKING:
    from disnake import Member


@dataclass
class ResultSet(AbstractCollection[Result]):
    @classmethod
    def from_result(cls, results: list, requester: Member | None = None) -> ResultSet:
        result_set: list[Result] = []
        for r in results:
            tmp: Result = Result(r)
            tmp.requester = requester
            result_set.append(tmp)

        return cls(set=result_set)

    @classmethod
    def empty(cls):
        return cls(set=[])

    def get(self) -> Result:
        return self.set.pop(0)

    def put(self, result: Result | ResultSet) -> None:
        if isinstance(result, ResultSet):
            self.set += result
        else:
            self.set.append(result)

    def add(self, result: Result | ResultSet) -> None:
        if isinstance(result, ResultSet):
            self.set[0:0] = result[::-1]
        else:
            self.set.insert(0, result)

    def remove(self, elem: str) -> Result | None:
        elem = elem.lower()
        for i, e in enumerate(self.set):
            if e.title.lower() == elem:
                return self.set.pop(i)
        return None

    def is_empty(self) -> bool:
        return len(self.set) == 0

    def shuffle(self) -> None:
        random.shuffle(self.set)
