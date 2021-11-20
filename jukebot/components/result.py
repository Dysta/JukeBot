from dataclasses import dataclass
from typing import Optional, Union

from jukebot.components import Query
from jukebot.utils import converter


@dataclass
class Result:
    id: Optional[Union[str, int]]
    url: str
    title: str
    channel: str
    duration: int = 0
    fmt_duration: str = "0:00"
    live: bool = False

    def __init__(self, info: dict):
        self.url = info["url"]
        self.id = info.get("id", -1)
        self.title = info.get("title", "Unknown")
        self.channel = info.get("channel", info.get("uploader", "Unknown"))
        self.duration = int(info.get("duration", 0) or 0)
        self.live = info.get("duration") is None
        self.fmt_duration = (
            "ထ" if self.live else converter.seconds_to_youtube_format(self.duration)
        )

    @classmethod
    def from_query(cls, query: Query, entry: int = 0):
        info = query.get_entries(entry) if "entries" in query.info else query.info
        return cls(info=info)

    @classmethod
    def from_entry(cls, entry: dict):
        return cls(info=entry)
