import datetime
import logging
import os
from typing import Set

from nextcord import Game
from nextcord.ext import commands

from dotenv import load_dotenv

from loguru import logger

from jukebot.utils import Extensions, intents, Environment
from jukebot import JukeBot
from jukebot.listeners import HelpHandler, InterceptHandler


def set_logging(
    intercept_nextcord_log: bool = True, nextcord_loglevel: int = logging.INFO
):
    logger.info(f"Environment is set to '{os.environ['environment']}'.")

    if intercept_nextcord_log:
        logger.info(
            f"Intercepting nextcord log messages with level {nextcord_loglevel}."
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=nextcord_loglevel)

    if os.environ["environment"] == Environment.DEVELOPMENT:
        pass
    elif os.environ["environment"] == Environment.PRODUCTION:
        logger.remove()
        fmt = "{time:YYYY-MM-DD at HH:mm:ss}:{level}:{name}: {message}"
        logger.add(
            f"./logs/log-{datetime.datetime.now():%Y-%m-%d}.log",
            level="INFO",
            format=fmt,
            rotation="01:00",
            retention="10 days",
            enqueue=True,
            mode="w",
            encoding="utf-8",
        )
    else:
        logger.error(f"Unknown environment {os.environ['environment']}.")
        exit(1)


async def prefix_for(client, message):
    prefixes = client.prefixes
    guild_id = message.guild.id
    if (prefix := await prefixes.get_item(guild_id)) is None:
        await prefixes.set_item(guild_id, os.environ["BOT_PREFIX"])
        prefix = os.environ["BOT_PREFIX"]
    logger.opt(lazy=True).debug(
        f"Return prefix '{prefix}' for guild {message.guild} (ID: {guild_id})"
    )
    return prefix


async def get_prefix(client, message):
    prefix = await prefix_for(client, message)
    return commands.when_mentioned_or(prefix)(client, message)


def get_ids() -> Set[int]:
    ids = os.environ["BOT_OWNER_IDS"].split(",")
    return set(map(int, ids))


def main():
    load_dotenv()
    set_logging(intercept_nextcord_log=False, nextcord_loglevel=logging.INFO)

    bot = JukeBot(
        command_prefix=get_prefix,
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
