from dataclasses import dataclass
from typing import Optional, Any

from jukebot.components import Request
from jukebot.utils import converter


@dataclass
class Song:
    id: str = Optional[str]
    title: str = Optional[str]
    stream_url: str = Optional[str]
    web_url: str = Optional[str]
    thumbnail: str = Optional[str]
    channel: str = Optional[str]
    duration: int = 0
    fmt_duration: str = "0:00"
    success: bool = False
    live: Any = None

    def __init__(self, info: dict):
        self.stream_url = info["url"]
        self.id = info.get("id", -1)
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
    def from_request(cls, request: Request, entry: int = 0):
        info = request.get_entries(entry) if "entries" in request.info else request.info
        return cls(info=info)

    @classmethod
    def from_entry(cls, entry: dict):
        return cls(info=entry)
