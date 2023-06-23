from __future__ import annotations

from disnake import CommandInteraction, Embed

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class ShuffleService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction):
        self.bot.players[interaction.guild.id].queue.shuffle()
        e: Embed = embed.basic_message(title="Queue shuffled.")
        await interaction.send(embed=e)
