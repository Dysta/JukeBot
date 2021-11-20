from dataclasses import dataclass
from typing import List

from jukebot.abstract_components import AbstractSet
from jukebot.components import Song, Query


@dataclass
class SongSet(AbstractSet[Song]):
    @classmethod
    def from_query(cls, query: Query) -> "SongSet":
        songs: List[Song] = []
        for e in query.entries:
            songs.append(Song.from_entry(e))

        return cls(set=songs)
