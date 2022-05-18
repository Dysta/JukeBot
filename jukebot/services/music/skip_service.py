from __future__ import annotations

from typing import Optional

from disnake import CommandInteraction

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class SkipService(AbstractService):
    async def __call__(
        self, /, interaction: CommandInteraction, silent: Optional[bool] = False
    ):
        self.bot.players[interaction.guild.id].skip()
        if not silent:
            e: embed = embed.basic_message(interaction.author, title="Skipped !")
            await interaction.send(embed=e)
