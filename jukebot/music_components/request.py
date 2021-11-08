import asyncio
import concurrent.futures

import youtube_dl
import json
import utils

from typing import Optional, Any

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ""


class Request:
    def __init__(self, query: str):
        self._query: str = query
        self._info: dict = {}
        self._id: str = Optional[str]
        self._title: str = Optional[str]
        self._url: str = Optional[str]
        self._web_url: str = Optional[str]
        self._thumbnail: str = Optional[str]
        self._channel: str = Optional[str]
        self._duration: int = 0
        self._success: bool = False
        self._live: Any = None

    async def process(self):
        ytdl_kwargs = dict(
            download=False,
            ie_key=None,
            extra_info={},
            process=True,
            force_generic_extractor=False,
        )
        with youtube_dl.YoutubeDL(_RequestOption.YTDL_FORMAT_OPTION) as ytdl:
            ytdl.cache.remove()

            def downloader(**ytdl_kwargs):
                return ytdl.extract_info(url=self._query, **ytdl_kwargs)

            info = await asyncio.to_thread(downloader, **ytdl_kwargs)

        with open("debug.json", "w") as f:
            json.dump(info, f)

        self._info = info["entries"][0] if "entries" in info else info
        self._url = self._info["url"]
        self._id = self._info.get("id", -1)
        self._title = self._info.get("title", "Unknown")
        self._duration = int(self._info.get("duration", 0))
        self._thumbnail = self._info.get("thumbnail", None)
        self._channel = self._info.get("channel", self._info.get("uploader", "Unknown"))
        self._web_url = self._info.get("webpage_url", "")
        self._live = self._info.get("is_live", False)
        self._success = True

    @property
    def success(self):
        return self._success

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def duration(self):
        return self._duration

    @property
    def web_url(self):
        return self._web_url

    @property
    def thumbnail(self):
        return self._thumbnail

    @property
    def id(self):
        return self._id

    @property
    def channel(self):
        return self._channel

    @property
    def live(self):
        return self._live


class _RequestOption:
    YTDL_FORMAT_OPTION: dict = {
        "format": "bestaudio/best",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
        "usenetrc": True,
    }
