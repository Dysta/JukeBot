from __future__ import annotations

import random
from typing import TYPE_CHECKING

import yaml
from aiofiles import open as aiopen
from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import BucketType
from loguru import logger

from jukebot.utils import checks
from jukebot.views.embed import error_message, music_message

if TYPE_CHECKING:
    from disnake import Embed

    from jukebot import JukeBot


class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot: JukeBot = bot
        self._radios: dict = {}

    async def cog_load(self) -> None:
        async with aiopen("./data/radios.yaml", "r") as f:
            content = await f.read()
            self._radios = yaml.safe_load(content)

    @commands.slash_command(description="Launch a random radio")
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.user_is_connected)
    async def radio(self, inter: CommandInteraction, radio: str):
        if not inter.response.is_done():
            await inter.response.defer()

        choices: list = self._radios.get(radio, [])
        if not choices:
            e: Embed = error_message(content=f"No radio found with the name `{radio}`")
            await inter.edit_original_message(embed=e)
            return

        query: str = random.choice(choices)
        logger.opt(lazy=True).debug(f"Choice is {query}")
        song, loop = await self.bot.services.play(interaction=inter, query=query, top=True)

        e: Embed = music_message(song, loop)
        await inter.edit_original_message(embed=e)

    @radio.autocomplete("radio")
    async def radio_autocomplete(self, inter: CommandInteraction, query: str):
        return [e for e in self._radios if query in e.lower()][:25]


def setup(bot: JukeBot):
    bot.add_cog(Radio(bot))
