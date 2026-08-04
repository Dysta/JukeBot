import asyncio
import random
import string
import tempfile
from pathlib import Path
from typing import ClassVar

import yt_dlp
from loguru import logger
from shazamio import Serialize, Shazam

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

    YTDL_BASE_OPTIONS: ClassVar[dict] = {
        "format": "bestaudio/best",
        "download_ranges": lambda _info, _ydl: ({"start_time": 0, "end_time": 30},),
        "nopart": True,
        "cachedir": False,
        "logger": _QueryLogger(),
    }

    def __init__(self, query: str):
        super().__init__(query=query)
        self._params: dict = {**ShazamRequest.YTDL_BASE_OPTIONS}
        self._delete_path: bool = False
        self._path: Path

    async def setup(self):
        rdm_str: str = "".join(random.choices(string.hexdigits, k=12))
        self._path = Path(tempfile.mkdtemp(prefix="jukebot-"), rdm_str)
        self._params.update({"outtmpl": self._path.as_posix()})

        logger.opt(lazy=True).debug(f"Generated path {self._path} with parameters {self._params}")

    async def execute(self):
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
        out = await shazam.recognize(data=str(self._path))
        result = Serialize.full_track(data=out)
        logger.debug(result.track)
        if not result.track:
            return

        if result.track.youtube_link:
            youtube_data = await shazam.get_youtube_data(link=result.track.youtube_link)
            data: dict = {
                "title": youtube_data["caption"],
                "url": youtube_data["actions"][0]["uri"],
                "image_url": youtube_data["image"]["url"],
            }
        else:
            with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ytdl:
                youtube_result = await asyncio.get_running_loop().run_in_executor(
                    None,
                    lambda: ytdl.extract_info(
                        f"ytsearch1:{result.track.subtitle} {result.track.title}",
                        download=False,
                    ),
                )
            video = youtube_result["entries"][0]
            video_id = video["id"]
            data = {
                "title": video["title"],
                "url": f"https://youtu.be/{video_id}?autoplay=1",
                "image_url": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
            }

        self._result = data
        self._success = True

        logger.opt(lazy=True).debug(f"Query data {self._result}")

    async def terminate(self):
        if self._delete_path:
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(None, lambda: self._path.unlink())
                await loop.run_in_executor(None, lambda: self._path.parent.rmdir())
                logger.opt(lazy=True).info(f"Temp folder for query {self._query} deleted at {self._path}")
            except Exception as e:
                logger.error(e)
