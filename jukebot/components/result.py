from dataclasses import dataclass

from .query import Query
from jukebot.utils import converter


@dataclass
class Result:
    web_url: str
    title: str
    channel: str
    duration: int = 0
    fmt_duration: str = "0:00"
    live: bool = False

    def __init__(self, info: dict):
        self.web_url = info["url"]
        self.title = info.get("title", "Unknown")
        self.channel = info.get("channel", info.get("uploader", "Unknown"))
        self.duration = int(info.get("duration", 0) or 0)
        self.live = info.get("duration") is None
        self.fmt_duration = (
            "ထ" if self.live else converter.seconds_to_youtube_format(self.duration)
        )

    @classmethod
    def from_query(cls, query: Query, entry: int = 0):
        # when query is called with .search(self), entries is a iterator
        # so we convert it to a list
        entries: list = list(query.entries)
        try:
            info = entries[entry]
        except KeyError:
            raise

        return cls(info=info)

    @classmethod
    def from_entry(cls, entry: dict):
        return cls(info=entry)
