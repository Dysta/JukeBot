from __future__ import annotations

import random
from typing import TYPE_CHECKING

import yaml
from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import BucketType
from loguru import logger

from jukebot.services.music import PlayService
from jukebot.utils import checks, embed

if TYPE_CHECKING:
    from disnake import Embed
    from disnake.ext.commands import Bot


class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self._radios: dict = {}

    async def cog_load(self) -> None:
        # ? we transform a list of dict into a single dict
        with open("./data/radios.yaml", "r") as f:
            data = yaml.safe_load(f)
            for e in data:
                self._radios.update(e)
        logger.debug(self._radios)

    async def _radio_process(self, inter: CommandInteraction, choices: list):
        query: str = random.choice(choices)
        logger.opt(lazy=True).debug(f"Choice is {query}")
        with PlayService(self.bot) as ps:
            await ps(interaction=inter, query=query, top=True)

    @commands.slash_command(description="Launch a random radio")
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.user_is_connected)
    async def radio(self, inter: CommandInteraction, radio: str):
        # TODO: check why there's no response when nothing is found
        choices: list = self._radios.get(radio, [])
        if not choices:
            e: Embed = embed.error_message(content=f"No radio found with the name `{radio}`")
            await inter.send(embed=e)
            return

        await self._radio_process(inter, choices)


def setup(bot):
    bot.add_cog(Radio(bot))
