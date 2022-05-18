from __future__ import annotations

from typing import Optional

from disnake import CommandInteraction

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class PauseService(AbstractService):
    async def __call__(
        self, /, interaction: CommandInteraction, silent: Optional[bool] = False
    ):
        self.bot.players[interaction.guild.id].pause()
        if not silent:
            e = embed.basic_message(interaction.author, title="Player paused")
            await interaction.send(embed=e)
