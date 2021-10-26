import datetime
import logging

from discord.ext import commands

from dotenv import load_dotenv
from jukebot import JukeBot
import os

from cogs import Utility
from listeners import ErrorHandler, HelpHandler


def main():
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

    load_dotenv()
    # get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value.
    # to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link
    # to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging
    # the flask server enjoy!
    bot = JukeBot(
        command_prefix=commands.when_mentioned_or(os.environ["BOT_PREFIX"]),
        help_command=HelpHandler(),
    )
    bot.add_cog(ErrorHandler(bot))
    bot.add_cog(Utility(bot))
    bot.help_command.cog = bot.get_cog("Utility")
    bot.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    main()
