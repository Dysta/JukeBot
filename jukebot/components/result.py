from dataclasses import dataclass
from typing import Optional, Union

from jukebot.components import Request
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
    def from_request(cls, request: Request, entry: int = 0):
        info = request.get_entries(entry) if "entries" in request.info else request.info
        return cls(info=info)

    @classmethod
    def from_entry(cls, entry: dict):
        return cls(info=entry)
