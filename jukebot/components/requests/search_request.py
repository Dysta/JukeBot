import asyncio

import yt_dlp
from loguru import logger

from jukebot.abstract_components import AbstractRequest
from jukebot.utils import regex


class SearchRequest(AbstractRequest):
    """Class that represent a search request.
    Search request are done during the search command and only here.
    Search request retrieve the 10 first track from a query on youtube or soundcloud website.
    Search request can retrive only 10 tracks, not playlist or sets.
    Search request canno't be created with url, only a query of words.
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

    def __init__(self, query: str, engine: str) -> None:
        if regex.is_url(query):
            raise ValueError(f"query must be words, not direct url")

        super().__init__(f"{engine}{query}")
        self._engine: str = engine
        self._params: dict = {**SearchRequest.YTDL_OPTIONS}

        self._process: bool = False

    async def setup(self):
        self._process = "sc" in self._engine
        logger.opt(lazy=True).debug(f"Query {self._query} have process state at {self._process}.")

    async def execute(self):
        with yt_dlp.YoutubeDL(params=self._params) as ytdl:
            loop = asyncio.get_event_loop()
            try:
                data = await loop.run_in_executor(
                    None,
                    lambda: ytdl.extract_info(
                        url=self._query, download=False, process=self._process
                    ),
                )
            except Exception as e:
                logger.error(f"Exception in query {self._query}. {e}")
                return

            self._result = data

    async def terminate(self):
        if not self._result:
            logger.opt(lazy=True).debug(f"No info retrieved for query {self._query}")
            return

        if not "entries" in self._result:
            # ? SearchRequest have to retrieved a playlist,
            # ? this shouldn't happen so we delete the result
            logger.warning(
                f"Query {self._query} don't retrieve a playlist. Deleleting the result."
            )
            self._result = None
            return

        self._result = list(self._result.pop("entries"))
        if not len(self._result):
            logger.warning(
                f"Query {self._query} don't retrieve any results. Deleleting the result."
            )
            self._result = None
            return

        self._success = True
