from __future__ import annotations

from disnake import CommandInteraction

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class LeaveService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction):
        # once the bot leave, we destroy is instance from the container
        await self.bot.players.pop(interaction.guild.id).disconnect()
        e = embed.basic_message(interaction.author, title="Player disconnected")
        await interaction.send(embed=e)
