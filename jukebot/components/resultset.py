from collections import abc
from dataclasses import dataclass
from typing import Iterator, List

from jukebot.components import Result, Query


@dataclass
class ResultSet(abc.Collection):
    results: List[Result]

    def __len__(self) -> int:
        return len(self.results)

    def __iter__(self) -> Iterator[Result]:
        for r in self.results:
            yield r

    def __contains__(self, r: object) -> bool:
        return r in self.results

    def __getitem__(self, idx: int) -> Result:
        if 0 <= idx < len(self):
            return self.results[idx]
        raise IndexError

    @classmethod
    def from_query(cls, query: Query) -> "ResultSet":
        results: List[Result] = []
        for r in query.entries:
            results.append(Result.from_entry(r))

        return cls(results=results)
