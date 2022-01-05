import asyncio
from enum import Enum

import yt_dlp

from typing import Optional, Union

# Silence useless bug reports messages
yt_dlp.utils.bug_reports_message = lambda: ""


class Query:
    class Type(Enum):
        TRACK = 0
        PLAYLIST = 1
        UNKNOWN = 2

    def __init__(self, query: str):
        self._query: str = query
        self._result: Optional[Union[dict, list]] = None
        self._success: bool = False
        self._type: Optional[Query.Type] = None

    async def search(self):
        await self._get(process=False)

    async def process(self):
        await self._get(process=True)

    async def _get(self, process: bool = True):
        ytdl_kwargs = dict(
            download=False,
            process=process,
        )
        with yt_dlp.YoutubeDL(params=_RequestOption.YTDL_FORMAT_OPTION) as ytdl:
            ytdl.cache.remove()

            loop = asyncio.get_event_loop()
            try:
                info = await loop.run_in_executor(
                    None, lambda: ytdl.extract_info(url=self._query, **ytdl_kwargs)
                )
            except:
                self._success = False
                return

        info = Query._sanitize_info(info)
        type = Query._define_type(info)

        # with open("debug.json", "w") as f:
        #     json.dump(info, f)
        self._result = info
        self._type = type
        self._success = self._type != Query.Type.UNKNOWN

    @staticmethod
    def _define_type(info: Union[dict, list]) -> "Query.Type":
        if isinstance(info, dict):
            return Query.Type.TRACK
        elif isinstance(info, list):
            return Query.Type.PLAYLIST
        else:
            return Query.Type.UNKNOWN

    @staticmethod
    def _sanitize_info(info: dict) -> Union[dict, list]:
        if "entries" in info:
            info = list(info["entries"])
            if len(info) == 1:
                info = info[0]
        return info

    @property
    def success(self):
        return self._success

    @property
    def results(self) -> list:
        return self._result

    @property
    def type(self) -> "Query.Type":
        return self._type


class _RequestOption:
    YTDL_FORMAT_OPTION: dict = {
        "format": "bestaudio/best",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "playlistend": 10,
        "max_downloads": 10,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
        "usenetrc": True,
        "socket_timeout": 3,
        # "skip_download": True,
    }
