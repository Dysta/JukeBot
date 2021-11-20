from dataclasses import dataclass
from typing import List

from jukebot.abstract_components import AbstractSet
from jukebot.components import Result, Query


@dataclass
class ResultSet(AbstractSet[Result]):
    @classmethod
    def from_query(cls, query: Query) -> "ResultSet":
        results: List[Result] = []
        for r in query.entries:
            results.append(Result.from_entry(r))

        return cls(set=results)
