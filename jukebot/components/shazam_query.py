import asyncio
import os
import random
import string
import tempfile
from pathlib import Path
from typing import Optional

import yt_dlp
from loguru import logger
from shazamio import Serialize, Shazam
from shazamio.models import YoutubeData

# Silence useless bug reports messages
yt_dlp.utils.bug_reports_message = lambda: ""


class ShazamQuery:
    def __init__(self, query: str):
        self._query: str = query
        self._success: bool = False
        self._info: Optional[YoutubeData] = None
        self._path: str = ""

        self._generate_path()

    def _generate_path(self) -> None:
        rdm_str: str = "".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
        )
        self._path = Path(tempfile.gettempdir(), "jukebot", rdm_str)
        logger.opt(lazy=True).debug(f"path {self._path}")

    async def process(self):
        params: dict = {"outtmpl": f"{self._path}"}
        params.update(_RequestOption.YTDL_FORMAT_OPTION)
        logger.opt(lazy=True).debug(params)

        with yt_dlp.YoutubeDL(params=params) as ytdl:
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(
                    None,
                    lambda: ytdl.download(self._query),
                )
            except Exception as e:
                logger.opt(lazy=True).error(e)
                self._success = False
                return

        shazam = Shazam()
        out = await shazam.recognize_song(data=self._path)
        result = Serialize.full_track(data=out)
        logger.debug(result)
        if not result.track:
            self._success = False
            return

        youtube_data = await shazam.get_youtube_data(link=result.track.youtube_link)
        self._info = Serialize.youtube(youtube_data)
        self._success = True
        logger.opt(lazy=True).debug(f"Query {self._query} saved at {self._path}")
        logger.opt(lazy=True).debug(f"Query data {self._info}")

    @property
    def success(self) -> bool:
        return self._success

    @property
    def info(self) -> Optional[YoutubeData]:
        return self._info

    async def delete_file(self) -> None:
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, lambda: os.remove(self._path))
            logger.opt(lazy=True).info(f"Query {self._query} deleted at {self._path}")
        except Exception as e:
            logger.error(e)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.delete_file()


class _QueryLogger:
    def debug(self, msg) -> None:
        if msg.startswith("[debug] "):
            logger.opt(lazy=True).debug(msg)
        else:
            self.info(msg)

    def info(self, msg) -> None:
        if len(msg) > 1:
            logger.opt(lazy=True).info(msg)

    def warning(self, msg) -> None:
        logger.opt(lazy=True).warning(msg)

    def error(self, msg) -> None:
        logger.opt(lazy=True).error(msg)


class _RequestOption:
    YTDL_FORMAT_OPTION: dict = {
        "format": "bestaudio/best",
        "external_downloader": "ffmpeg",
        "external_downloader_args": {
            "ffmpeg_i": ["-vn", "-ss", "00:00", "-to", "00:30"],
            "ffmpeg": ["-t", "20"],
        },
        "nopart": True,
        "cachedir": False,
        "logger": _QueryLogger(),
    }
