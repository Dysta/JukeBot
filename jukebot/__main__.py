import logging as plogging
import os
from typing import Set

from nextcord import Game
from nextcord.ext import commands

from dotenv import load_dotenv

from loguru import logger

from jukebot.utils import Extensions, intents, logging, prefix
from jukebot import JukeBot
from jukebot.listeners import HelpHandler


def get_ids() -> Set[int]:
    ids = os.environ["BOT_OWNER_IDS"].split(",")
    return set(map(int, ids))


def main():
    load_dotenv()
    logging.set_logging(intercept_nextcord_log=True, nextcord_loglevel=plogging.WARNING)

    bot = JukeBot(
        command_prefix=prefix.get_prefix,
        help_command=HelpHandler(),
        activity=Game(f"{os.environ['BOT_PREFIX']}help"),
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
    main()
