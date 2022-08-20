from __future__ import annotations

import asyncio
from enum import Enum
from typing import Optional, Union

import yt_dlp
from loguru import logger

# Silence useless bug reports messages
yt_dlp.utils.bug_reports_message = lambda: ""


class Query:
    class Type(Enum):
        TRACK = 0
        PLAYLIST = 1
        UNKNOWN = 2

    def __init__(self, query: str):
        self._query: str = query
        self._result: Optional[Union[dict, list]] = None
        self._success: bool = False
        self._type: Optional[Query.Type] = None

    async def search(self):
        await self._get(process=False)

    async def process(self):
        await self._get(process=True)

    async def _get(self, process: bool = True):
        with yt_dlp.YoutubeDL(params=_RequestOption.YTDL_FORMAT_OPTION) as ytdl:
            loop = asyncio.get_event_loop()
            try:
                info = await loop.run_in_executor(
                    None,
                    lambda: ytdl.extract_info(url=self._query, download=False, process=process),
                )
            except Exception as e:
                logger.opt(lazy=True).error(f"Exception in query {self._query}. {e}")
                self._success = False
                return

        if not info:
            logger.opt(lazy=True).debug(f"No info retrieved for query {self._query}")
            self._success = False
            return

        if False:
            # fmt: off
            import json
            with open("debug.json", "w") as f:
                json.dump(ytdl.sanitize_info(info), f)
            # fmt: on

        info = Query._sanitize_info(info)
        type = Query._define_type(info)

        if isinstance(info, list) and len(info) == 0:
            logger.opt(lazy=True).debug(f"No info retrieved for query {self._query}")
            self._success = False
            return

        self._result = info
        self._type = type
        self._success = self._type != Query.Type.UNKNOWN
        logger.opt(lazy=True).debug(f"Retrieve music '{info}' for query {self._query}")

    @staticmethod
    def _define_type(info: Union[dict, list]) -> "Query.Type":
        if isinstance(info, dict):
            return Query.Type.TRACK
        elif isinstance(info, list):
            return Query.Type.PLAYLIST
        else:
            return Query.Type.UNKNOWN

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

    @property
    def type(self) -> "Query.Type":
        return self._type


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
        "compat_opts": ["no-youtube-unavailable-videos"],
        "noplaylist": True,
        "cachedir": False,
        # "logger": _QueryLogger(),
    }
