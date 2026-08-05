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
        self._path: Path | None = None

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

        logger.opt(lazy=True).debug(f"Query {self._query} saved at {self._path}")
        shazam = Shazam()
        out = await shazam.recognize(data=str(self._path))
        result = Serialize.full_track(data=out)
        logger.debug(result.track)
        if not result.track:
            return

        image_url = result.track.photo_url or next(
            (
                page.image
                for section in result.track.sections
                for page in reversed(getattr(section, "meta_pages", []))
                if page.image
            ),
            None,
        )
        spotify_url = result.track.spotify_url
        if spotify_url and spotify_url.startswith("spotify:search:"):
            spotify_url = spotify_url.replace("spotify:search:", "https://open.spotify.com/search/", 1)

        apple_music_url = result.track.apple_music_url
        if apple_music_url and apple_music_url.startswith("intent://"):
            apple_music_url = f"https://{apple_music_url.removeprefix('intent://').split('#', 1)[0]}"

        links = {
            name: url
            for name, url in {
                "Apple Music": apple_music_url,
                "Spotify": spotify_url,
                "YouTube": result.track.youtube_link,
            }.items()
            if url
        }

        data: dict = {
            "title": result.track.title,
            "author": result.track.subtitle,
            "url": next(iter(links.values()), None),
            "image_url": image_url,
            "links": links,
        }

        self._result = data
        self._success = True

        logger.opt(lazy=True).debug(f"Query data {self._result}")

    async def terminate(self):
        def _clean(path: Path):
            path.unlink(missing_ok=True)
            path.parent.rmdir()

        if self._path:
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(None, _clean, self._path)
                logger.opt(lazy=True).info(f"Temp folder for query {self._query} deleted at {self._path}")
            except Exception as e:
                logger.error(e)
