import asyncio
import yt_dlp

from typing import Optional, Any

# Silence useless bug reports messages
yt_dlp.utils.bug_reports_message = lambda: ""


class Request:
    def __init__(self, query: str):
        self._query: str = query
        self._info: dict = {}
        self._id: str = Optional[str]
        self._title: str = Optional[str]
        self._stream_url: str = Optional[str]
        self._web_url: str = Optional[str]
        self._thumbnail: str = Optional[str]
        self._channel: str = Optional[str]
        self._duration: int = 0
        self._fmt_duration: str = "0:00"
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
        with yt_dlp.YoutubeDL(_RequestOption.YTDL_FORMAT_OPTION) as ytdl:
            ytdl.cache.remove()

            def downloader(**ytdl_kwargs):
                return ytdl.extract_info(url=self._query, **ytdl_kwargs)

            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: downloader(**ytdl_kwargs))

        # with open("debug.json", "w") as f:
        #     json.dump(info, f)

        self._info = info
        self._success = True

    def get_entries(self, number: int):
        if "entries" in self._info:
            try:
                return self._info["entries"][number]
            except KeyError:
                raise
        return self._info

    @property
    def success(self):
        return self._success

    @property
    def info(self):
        return self._info

    @property
    def entries(self):
        if "entries" in self._info:
            return self._info["entries"]
        return [self._info]


class _RequestOption:
    YTDL_FORMAT_OPTION: dict = {
        "format": "bestaudio/best",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "playlistend": 10,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
        "usenetrc": True,
        "socket_timeout": 3,
    }
