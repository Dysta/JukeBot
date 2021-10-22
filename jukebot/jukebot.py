import discord

from embed import Embed
from discord.ext import commands


class JukeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._activity = discord.Game("Juke goes brrr")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        await self.change_presence(
            status=discord.Status.online, activity=self._activity
        )

    async def on_error(self, event, *args, **kwargs):
        print(f"{event=}")

    async def on_command_error(self, ctx, exception):
        print(f"{exception=}")
        e = Embed.error_message(content=exception)
