import datetime
import logging
import os
from typing import Set

from nextcord import Game
from nextcord.ext import commands

from dotenv import load_dotenv

from jukebot.utils import Extensions, intents
from jukebot import JukeBot
from jukebot.listeners import HelpHandler


def set_logging():
    logger = logging.getLogger("nextcord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename=f"./logs/{datetime.datetime.now():%Y-%m-%d}-jukebot.log",
        encoding="utf-8",
        mode="w",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)


async def prefix_for(client, message):
    prefixes = client.prefixes
    guild_id = message.guild.id
    if (prefix := await prefixes.get_item(guild_id)) is None:
        await prefixes.set_item(guild_id, os.environ["BOT_PREFIX"])
        prefix = os.environ["BOT_PREFIX"]
    return prefix


async def get_prefix(client, message):
    prefix = await prefix_for(client, message)
    return commands.when_mentioned_or(prefix)(client, message)


def get_ids() -> Set[int]:
    ids = os.environ["BOT_OWNER_IDS"].split(",")
    return set(map(int, ids))


def main():
    load_dotenv()
    set_logging()

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
        except commands.ExtensionNotFound as e:
            print(e)

    bot.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    main()
