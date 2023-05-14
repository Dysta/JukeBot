from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from disnake import Member

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
    requester: Optional[Member] = None

    def __init__(self, info: dict):
        self.stream_url = info["url"]
        self.title = info.get("title", "Unknown")
        self.live = info.get("is_live", False)
        self.duration = round(info.get("duration") or 0)
        self.fmt_duration = (
            "ထ" if self.live else converter.seconds_to_youtube_format(self.duration)
        )
        self.thumbnail = info.get("thumbnail", None)
        self.channel = info.get("channel") or info.get("uploader") or "Unknown"
        self.web_url = info.get("webpage_url", "")
