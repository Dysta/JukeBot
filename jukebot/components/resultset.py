import random

from dataclasses import dataclass
from typing import List, Optional

from nextcord import Member

from jukebot.abstract_components import AbstractCollection
from .result import Result
from .query import Query


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

    def remove(self, idx: int) -> Optional[Result]:
        try:
            e = self.set.pop(idx)
        except:
            return None
        return e

    def is_empty(self) -> bool:
        return len(self.set) == 0

    def shuffle(self) -> None:
        random.shuffle(self.set)
