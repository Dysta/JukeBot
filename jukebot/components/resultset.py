from dataclasses import dataclass
from typing import List

from jukebot.abstract_components import AbstractSet
from .result import Result
from .query import Query


@dataclass
class ResultSet(AbstractSet[Result]):
    @classmethod
    def from_query(cls, query: Query) -> "ResultSet":
        results: List[Result] = []
        for r in query.entries:
            results.append(Result.from_entry(r))

        return cls(set=results)

    @classmethod
    def empty(cls):
        return cls(set=[])

    def get(self) -> Result:
        return self.set.pop(0)

    def put(self, result: Result) -> None:
        self.set.append(result)
