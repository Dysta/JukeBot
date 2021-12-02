from dataclasses import dataclass
from typing import List

from jukebot.abstract_components import AbstractSet
from jukebot.components import Song, Query


@dataclass
class SongSet(AbstractSet[Song]):
    @classmethod
    def from_query(cls, query: Query) -> "SongSet":
        song_set: List[Song] = []
        results = query.results
        if not isinstance(results, list):
            results = [query.results]
        for r in results:
            song_set.append(Song.from_entry(r))

        return cls(set=song_set)
