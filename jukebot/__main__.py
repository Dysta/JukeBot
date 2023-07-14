from __future__ import annotations

import logging as plogging
import os
import sys
from typing import List, Optional, Set

from disnake import Activity, ActivityType
from disnake.ext import commands
from dotenv import load_dotenv
from loguru import logger

from jukebot import JukeBot
from jukebot.utils import Extensions, intents, logging


def get_owner_ids() -> Set[int]:
    ids = os.environ["BOT_OWNER_IDS"].split(",")
    return set(map(int, ids))


def get_test_guilds_ids() -> Optional[List[int]]:
    ids = list(filter(lambda x: x, os.environ["BOT_TEST_GUILD_IDS"].split(",")))
    if not ids:
        return None
    return list(map(int, ids))


def main():
    load_dotenv(".env")
    logging.set_logging(
        plogging.getLevelName(os.environ["LOG_LEVEL"]),
        intercept_disnake_log=True,
        disnake_loglevel=plogging.getLevelName(os.environ["DISCORD_LOG_LEVEL"]),
    )

    bot = JukeBot(
        activity=Activity(name=f"some good vibes 🎶", type=ActivityType.listening),
        intents=intents.get(),
        owner_ids=get_owner_ids(),
        test_guilds=get_test_guilds_ids(),
    )

    for e in Extensions.all():
        try:
            bot.load_extension(name=f"{e['package']}.{e['name']}")
            logger.success(f"Extension '{e['package']}.{e['name']}' loaded")
        except commands.ExtensionNotFound as e:
            logger.error(e)

    logger.info(f"Starting bot...")
    bot.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    try:
        if not sys.platform in ("win32", "cygwin", "cli"):
            import uvloop

            uvloop.install()
    except ImportError:
        logger.opt(lazy=True).info("Bot launch without speed extra.")
    main()
