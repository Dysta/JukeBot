from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from disnake import Member

from jukebot.utils import converter


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
        self.web_url = info.get("url") or info.get("original_url")
        self.title = info.get("title", "Unknown")
        self.channel = info.get("channel") or info.get("uploader") or "Unknown"
        self.duration = round(info.get("duration") or 0)
        self.live = info.get("duration") is None
        self.fmt_duration = (
            "ထ" if self.live else converter.seconds_to_youtube_format(self.duration)
        )

        if self.title == "Unknown" or self.channel == "Unknwon":
            self._define_complementary_info_from_url()

    def _define_complementary_info_from_url(self):
        """This method try to define title and channel from url"""
        if "soundcloud" in self.web_url:
            # ? SoundCloud API return only the url
            # ? we try to define title and channel from it
            *_, tmp_channel, tmp_title = self.web_url.split("/")
            if self.channel == "Unknown":
                self.channel = tmp_channel.replace("-", " ").title()
            if self.title == "Unknown":
                self.title = tmp_title.replace("-", " ").title()
