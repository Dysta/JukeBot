from dotenv import load_dotenv
from jukebot import JukeBot
import os

from utility import Utiliy


def main():
    load_dotenv()
    # client.run(os.getenv("BETA_TOKEN")) #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value.
    # to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
    # enjoy!
    bot = JukeBot(command_prefix="!", help_message=None)
    bot.add_cog(Utiliy(bot))
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
