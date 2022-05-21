from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import CommandInteraction, Embed

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import Player


class ClearService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction):
        player: Player = self.bot.players[interaction.guild.id]
        player.queue = components.ResultSet.empty()

        e: Embed = embed.basic_message(
            interaction.author, title="The queue have been cleared."
        )
        await interaction.send(embed=e)
