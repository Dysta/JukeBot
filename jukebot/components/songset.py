from collections import abc
from dataclasses import dataclass
from typing import Iterator, List

from jukebot.components import Song, Request


@dataclass
class SongSet(abc.Collection):
    songs: List[Song]

    def __len__(self) -> int:
        return len(self.songs)

    def __iter__(self) -> Iterator[Song]:
        for s in self.songs:
            yield s

    def __contains__(self, s: object) -> bool:
        return s in self.songs

    def __getitem__(self, idx: int) -> Song:
        if 0 <= idx < len(self):
            return self.songs[idx]
        raise IndexError

    @classmethod
    def from_request(cls, request: Request) -> 'SongSet':
        songs: List[Song] = []
        for e in request.entries:
            songs.append(Song.from_entry(e))

        return cls(songs=songs)
