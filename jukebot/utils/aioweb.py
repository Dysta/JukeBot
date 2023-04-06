from __future__ import annotations

from urllib import parse

import aiohttp
import asyncstdlib as alib
from loguru import logger

_MOZ_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}


@alib.lru_cache(maxsize=1024)
async def cached_query(url, enquote_url: bool = False) -> (int, str):
    logger.opt(lazy=True).info(f"Cached query for url {url}")
    return await _get(url, enquote_url)


async def uncached_query(url, enquote_url: bool = False) -> (int, str):
    logger.opt(lazy=True).info(f"Uncached query for url {url}")
    return await _get(url, enquote_url)


async def _get(url, enquote) -> (int, str):
    url = url if not enquote else parse.quote(url)

    async with aiohttp.ClientSession(headers=_MOZ_HEADER) as session:
        async with session.get(url) as rep:
            logger.opt(lazy=True).info(f"Get url {url}")
            logger.opt(lazy=True).info(f"URL {url} status: {rep.status}")
            logger.opt(lazy=True).debug(f"URL {url} content-type: {rep.headers['content-type']}")
            if rep.status != 200:
                return rep.status, ""

            if "application/json" in rep.headers["content-type"]:
                return rep.status, await rep.json()
            return rep.status, await rep.text()
