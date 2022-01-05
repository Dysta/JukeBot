from dataclasses import dataclass
from typing import Optional

from nextcord import Member

from jukebot.utils import converter
from .query import Query


@dataclass
class Result:
    web_url: str
    title: str
    channel: str
    duration: int = 0
    fmt_duration: str = "0:00"
    live: bool = False
    requester: Optional[Member] = None

    def __init__(self, info: dict):
        self.web_url = info.get("url", info.get("original_url"))
        self.title = info.get("title", "Unknown")
        self.channel = info.get("channel", info.get("uploader", "Unknown"))
        self.duration = int(info.get("duration", 0) or 0)
        self.live = info.get("duration") is None
        self.fmt_duration = (
            "ထ" if self.live else converter.seconds_to_youtube_format(self.duration)
        )

    @classmethod
    def from_query(cls, query: Query, entry: int = 0):
        results = query.results
        if query.type == Query.Type.PLAYLIST:
            try:
                info = results[entry]
            except KeyError:
                raise
        elif query.type == Query.Type.TRACK:
            info = results
        else:
            raise Exception(f"Query result unknown format for {results=}")

        return cls(info=info)

    @classmethod
    def from_entry(cls, entry: dict):
        return cls(info=entry)
