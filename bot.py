import datetime
import logging
import os

from nextcord.ext import commands

from dotenv import load_dotenv

from jukebot.jukebot import PrefixCollection
from jukebot.utils import Extensions
from jukebot import JukeBot
from jukebot.listeners import HelpHandler


def main():
    load_dotenv()
    # setting up logging
    logger = logging.getLogger("discord")
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
        prefixes = PrefixCollection()
        try:
            prefix = prefixes[str(message.guild.id)]
        except KeyError:
            prefix = prefixes[str(message.guild.id)] = os.environ["BOT_PREFIX"]
        return prefix

    async def get_prefix(client, message):
        prefix = await prefix_for(client, message)
        return commands.when_mentioned_or(prefix)(client, message)

    bot = JukeBot(
        command_prefix=get_prefix,
        help_command=HelpHandler(),
    )

    for e in Extensions.all():
        try:
            bot.load_extension(name=f"{e['package']}.{e['name']}")
        except commands.ExtensionNotFound as e:
            print(e)

    bot.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    main()
