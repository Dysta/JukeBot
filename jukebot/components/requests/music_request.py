from __future__ import annotations

import asyncio
from enum import Enum, auto

import yt_dlp
from loguru import logger

from jukebot.abstract_components import AbstractRequest
from jukebot.utils import regex


class MusicRequest(AbstractRequest):
    """Class that represent a music request.
    Music request are done during the queue add command and only here.
    Music request can retrive a single tracks, a playlist or a set.
    Music request query can be made of an url.
    """

    class ResultType(Enum):
        """Define the type of the result

        Parameters
        ----------
        Enum : Enum
            The type of the result.
            Can be a single track, a playlist or an unknown format
        """

        TRACK = auto()
        PLAYLIST = auto()
        UNKNOWN = auto()

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
        self._type: MusicRequest.ResultType = MusicRequest.ResultType.UNKNOWN
        self._single_search: bool = False

    async def __aenter__(self):
        if not regex.is_url(self._query):
            self._query = f"ytsearch1:{self._query}"
            self._single_search = True

        return self

    async def __call__(self):
        with yt_dlp.YoutubeDL(params=self._params) as ytdl:
            loop = asyncio.get_event_loop()
            try:
                data = await loop.run_in_executor(
                    None,
                    lambda: ytdl.extract_info(url=self._query, download=False, process=False),
                )
            except Exception as e:
                logger.error(f"Exception in query {self._query}. {e}")
                return

            self._result = data

    async def __aexit__(self, exc_type, exc_value, traceback):
        if not self._result:
            logger.opt(lazy=True).debug(f"No info retrieved for query {self._query}")
            return

        if not "entries" in self._result:
            # ? MusicRequest returned an only track
            self._type = MusicRequest.ResultType.TRACK
            self._success = True
            return

        # ? assume that MusicRequest return a playlist
        self._result = list(self._result.pop("entries"))
        # ? check if result isn't an empty iterator
        if not len(self._result):
            self._result = None
            logger.opt(lazy=True).debug(f"No info retrieved for query {self._query}")
            return

        if self._single_search:
            self._result = self._result[0]
            self._type = MusicRequest.ResultType.TRACK
        else:
            self._type = MusicRequest.ResultType.PLAYLIST

        self._success = True

    @property
    def type(self) -> MusicRequest.ResultType:
        return self._type

    def _clean_data(self) -> None:
        """Remove useless data from the result"""
        useless_keys: list = ["formats", "thumbnails"]

        def inner(results) -> None:
            for e in useless_keys:
                if e in results:
                    results.pop(e)

        if isinstance(self._result, list):
            for r in self._result:
                inner(r)
        else:
            inner(self._result)
