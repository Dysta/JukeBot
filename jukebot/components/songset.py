from dataclasses import dataclass
from typing import List

from jukebot.abstract_components import AbstractCollection
from .query import Query
from .song import Song


@dataclass
class SongSet(AbstractCollection[Song]):
    @classmethod
    def from_query(cls, query: Query) -> "SongSet":
        song_set: List[Song] = []
        results = query.results
        if not query.type == Query.Type.PLAYLIST:
            results = [query.results]
        for r in results:
            song_set.append(Song.from_entry(r))

        return cls(set=song_set)
