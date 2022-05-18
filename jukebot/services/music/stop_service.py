from __future__ import annotations

from disnake import CommandInteraction

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class StopService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction):
        self.bot.players[interaction.guild.id].stop()
        e = embed.basic_message(interaction.author, title="Player stopped")
        await interaction.send(embed=e)
