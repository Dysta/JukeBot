from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional

from disnake import Member

from jukebot.abstract_components import AbstractCollection

from .query import Query
from .result import Result


@dataclass
class ResultSet(AbstractCollection[Result]):
    @classmethod
    def from_query(
        cls, query: Query, requester: Optional[Member] = None
    ) -> "ResultSet":
        result_set: List[Result] = []
        results = query.results
        if not query.type == Query.Type.PLAYLIST:
            results = [query.results]
        for r in results:
            rslt: Result = Result.from_entry(r)
            rslt.requester = requester
            result_set.append(rslt)

        return cls(set=result_set)

    @classmethod
    def empty(cls):
        return cls(set=[])

    def get(self) -> Result:
        return self.set.pop(0)

    def put(self, result: Result) -> None:
        self.set.append(result)

    def add(self, result: Result) -> None:
        self.set.insert(0, result)

    def remove(self, elem: str) -> Optional[Result]:
        for i, e in enumerate(self.set):
            if e.title.lower() == elem.lower():
                return self.set.pop(i)
        return None

    def is_empty(self) -> bool:
        return len(self.set) == 0

    def shuffle(self) -> None:
        random.shuffle(self.set)
