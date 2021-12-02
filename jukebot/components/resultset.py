from dataclasses import dataclass
from typing import List

from nextcord import Member

from jukebot.abstract_components import AbstractSet
from .result import Result
from .query import Query


@dataclass
class ResultSet(AbstractSet[Result]):
    @classmethod
    def from_query(cls, author: Member, query: Query) -> "ResultSet":
        result_set: List[Result] = []
        results = query.results
        if not isinstance(results, list):
            results = [query.results]
        for r in results:
            result_set.append(Result.from_entry(author, r))

        return cls(set=result_set)

    @classmethod
    def empty(cls):
        return cls(set=[])

    def get(self) -> Result:
        return self.set.pop(0)

    def put(self, result: Result) -> None:
        self.set.append(result)
