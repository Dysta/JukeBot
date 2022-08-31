import asyncio

import yt_dlp
from loguru import logger

from jukebot.abstract_components import AbstractRequest


class MusicRequest(AbstractRequest):
    """Class that represent a music request.
    Music request are done during the play command and only here.
    Music request retrieve all the data used by the bot to stream the audio in a given voice channel.
    Music request can retrive only one track, not playlist or sets.
    """

    YTDL_OPTIONS: dict = {
        "format": "bestaudio/best",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
        "usenetrc": True,
        "socket_timeout": 3,
        "noplaylist": True,
        "cachedir": False,
        # "logger": _QueryLogger(),
    }

    def __init__(self, query: str) -> None:
        super().__init__(query)
        self._params: dict = {**MusicRequest.YTDL_OPTIONS}

    async def setup(self):
        # * nothing to do
        pass

    async def execute(self):
        with yt_dlp.YoutubeDL(params=self._params) as ytdl:
            loop = asyncio.get_event_loop()
            try:
                data = await loop.run_in_executor(
                    None,
                    lambda: ytdl.extract_info(url=self._query, download=False),
                )
            except Exception as e:
                logger.error(f"Exception in query {self._query}. {e}")
                return

            self._result = data

    async def terminate(self):
        if not self._result:
            logger.opt(lazy=True).debug(f"No info retrieved for query {self._query}")
            return

        if "entries" in self._result:
            # ? MusicRequest have retrieved a playlist,
            # ? this shouldn't happen so we delete the result
            logger.warning(f"Query {self._query} retrieve a playlist. Deleleting the result.")
            self._result = None
            return

        self._success = True
