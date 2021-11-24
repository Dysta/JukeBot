from dataclasses import dataclass
from typing import Optional

from .query import Query
from jukebot.utils import converter


@dataclass
class Song:
    title: str = "Unknown"
    stream_url: Optional[str] = None
    web_url: str = ""
    thumbnail: Optional[str] = None
    channel: str = "Unknown"
    duration: int = 0
    fmt_duration: str = "0:00"
    live: bool = False

    def __init__(self, info: dict):
        self.stream_url = info["url"]
        self.title = info.get("title", "Unknown")
        self.live = info.get("is_live", False)
        self.duration = int(info.get("duration", 0)) if not self.live else 0
        self.fmt_duration = (
            "ထ" if self.live else converter.seconds_to_youtube_format(self.duration)
        )
        self.thumbnail = info.get("thumbnail", None)
        self.channel = info.get("channel", info.get("uploader", "Unknown"))
        self.web_url = info.get("webpage_url", "")

    @classmethod
    def from_query(cls, query: Query, entry: int = 0):
        info = query.get_entries(entry) if "entries" in query.info else query.info
        return cls(info=info)

    @classmethod
    def from_entry(cls, entry: dict):
        return cls(info=entry)
