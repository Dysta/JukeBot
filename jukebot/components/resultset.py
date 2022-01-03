from dataclasses import dataclass
from typing import List, Optional

from jukebot.abstract_components import AbstractCollection
from .result import Result
from .query import Query


@dataclass
class ResultSet(AbstractCollection[Result]):
    @classmethod
    def from_query(cls, query: Query) -> "ResultSet":
        result_set: List[Result] = []
        results = query.results
        if not isinstance(results, list):
            results = [query.results]
        for r in results:
            result_set.append(Result.from_entry(r))

        return cls(set=result_set)

    @classmethod
    def empty(cls):
        return cls(set=[])

    def get(self) -> Result:
        return self.set.pop(0)

    def put(self, result: Result) -> None:
        self.set.append(result)

    def remove(self, idx: int) -> Optional[Result]:
        try:
            e = self.set.pop(idx)
        except:
            return None
        return e
