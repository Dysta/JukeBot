from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from disnake import Member

from jukebot.abstract_components import AbstractCollection

from .song import Song


@dataclass
class SongSet(AbstractCollection[Song]):
    @classmethod
    def from_result(cls, results: list, requester: Optional[Member] = None) -> SongSet:
        result_set: List[Song] = []
        for r in results:
            tmp: Song = Song.from_entry(r)
            tmp.requester = requester
            result_set.append(tmp)

        return cls(set=result_set)
