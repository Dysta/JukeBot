import asyncio
from typing import Optional, Union

import yt_dlp

# Silence useless bug reports messages
yt_dlp.utils.bug_reports_message = lambda: ""


class Query:
    def __init__(self, query: str):
        self._query: str = query
        self._result: Optional[Union[dict, list]] = None
        self._success: bool = False

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
            info = await loop.run_in_executor(
                None, lambda: ytdl.extract_info(url=self._query, **ytdl_kwargs)
            )
            info = Query._sanitize_info(info)

        # with open("debug.json", "w") as f:
        #     json.dump(info, f)

        self._result = info
        self._success = True

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
