import asyncio

import yt_dlp

# Silence useless bug reports messages
yt_dlp.utils.bug_reports_message = lambda: ""


class Request:
    def __init__(self, query: str):
        self._query: str = query
        self._info: dict = {}
        self._success: bool = False
        self._extra_info: dict = {"id": -1, "title": "Unknown", "uploader": "Unknown"}

    async def search(self):
        await self._get(process=False)

    async def process(self):
        await self._get(process=True)

    async def _get(self, process: bool = True):
        ytdl_kwargs = dict(
            download=False,
            process=process,
            extra_info=self._extra_info if not process else None,
        )
        with yt_dlp.YoutubeDL(params=_RequestOption.YTDL_FORMAT_OPTION) as ytdl:
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
