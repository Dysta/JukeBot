import asyncio
import os
import random
import string
import tempfile
from pathlib import Path

import yt_dlp
from loguru import logger
from shazamio import Serialize, Shazam

# Silence useless bug reports messages
yt_dlp.utils.bug_reports_message = lambda: ""

from jukebot.abstract_components import AbstractRequest


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
        logger.warning(msg)

    def error(self, msg) -> None:
        logger.error(msg)


class ShazamRequest(AbstractRequest):
    """Class that represent a Shazam request.
    Shazam request are done during the find command and only here.
    Shazam request retrieve all the data to recognize a media given via an URL.
    Shazam request can retrive only one media, not playlist or sets
    """

    FILENAME_CHARS: str = string.ascii_letters + string.digits
    FILENAME_LENGHT: int = 8
    YTDL_BASE_OPTIONS: dict = {
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

    def __init__(self, query: str):
        super().__init__(query=query)
        self._path: str = ""
        self._params: dict = {**ShazamRequest.YTDL_BASE_OPTIONS}
        self._delete_path: bool = False

    async def __aenter__(self):
        rdm_str: str = "".join(
            [random.choice(ShazamRequest.FILENAME_CHARS) for _ in range(ShazamRequest.FILENAME_LENGHT)]
        )
        self._path = Path(tempfile.gettempdir(), "jukebot", rdm_str)
        self._params.update({"outtmpl": f"{self._path}"})

        logger.opt(lazy=True).debug(f"Generated path {self._path} with parameters {self._params}")

        return self

    async def __call__(self):
        with yt_dlp.YoutubeDL(params=self._params) as ytdl:
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(
                    None,
                    lambda: ytdl.download(self._query),
                )
            except Exception as e:
                logger.error(e)
                return

        self._delete_path = True
        logger.opt(lazy=True).debug(f"Query {self._query} saved at {self._path}")
        shazam = Shazam()
        out = await shazam.recognize_song(data=self._path)
        result = Serialize.full_track(data=out)
        logger.debug(result.track)
        if not result.track:
            return

        youtube_data = await shazam.get_youtube_data(link=result.track.youtube_link)
        data: dict = {
            "title": youtube_data["caption"],
            "url": youtube_data["actions"][0]["uri"],
            "image_url": youtube_data["image"]["url"],
        }

        self._result = data
        self._success = True

        logger.opt(lazy=True).debug(f"Query data {self._result}")

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._delete_path:
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(None, lambda: os.remove(self._path))
                logger.opt(lazy=True).info(f"Query {self._query} deleted at {self._path}")
            except Exception as e:
                logger.error(e)
