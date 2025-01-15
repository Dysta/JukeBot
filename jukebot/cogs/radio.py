from __future__ import annotations

import random
from typing import TYPE_CHECKING

from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import BucketType
from loguru import logger

from jukebot import JukeBot
from jukebot.utils import checks, converter, embed

if TYPE_CHECKING:
    from disnake import Embed


class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot: JukeBot = bot
        self._radios: dict = {}

    async def cog_load(self) -> None:
        self._radios = converter.radios_yaml_to_dict()

    async def _radio_process(self, inter: CommandInteraction, choices: list):
        query: str = random.choice(choices)
        logger.opt(lazy=True).debug(f"Choice is {query}")
        await self.bot.services.play(interaction=inter, query=query, top=True)

    @commands.slash_command(description="Launch a random radio")
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.user_is_connected)
    async def radio(self, inter: CommandInteraction, radio: str):
        choices: list = self._radios.get(radio, [])
        if not choices:
            e: Embed = embed.error_message(content=f"No radio found with the name `{radio}`")
            await inter.send(embed=e)
            return

        await self._radio_process(inter, choices)

    @radio.autocomplete("radio")
    async def radio_autocomplete(self, inter: CommandInteraction, query: str):
        return [e for e in self._radios.keys() if query in e.lower()][:25]


def setup(bot: JukeBot):
    bot.add_cog(Radio(bot))
