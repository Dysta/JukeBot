from __future__ import annotations

import logging as plogging
import os
import sys
from typing import Set

from disnake import Activity, ActivityType
from disnake.ext import commands
from dotenv import load_dotenv
from loguru import logger

from jukebot import JukeBot
from jukebot.listeners import HelpHandler
from jukebot.utils import Extensions, intents, logging, prefix


def get_ids() -> Set[int]:
    ids = os.environ["BOT_OWNER_IDS"].split(",")
    return set(map(int, ids))


def main():
    load_dotenv(".env")
    logging.set_logging(
        plogging.INFO,
        intercept_disnake_log=True,
        disnake_loglevel=plogging.WARNING,
    )

    bot = JukeBot(
        command_prefix=prefix.get_prefix,
        help_command=HelpHandler(),
        activity=Activity(
            name=f"{os.environ['BOT_PREFIX']}help", type=ActivityType.listening
        ),
        intents=intents.get(),
        owner_ids=get_ids(),
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
