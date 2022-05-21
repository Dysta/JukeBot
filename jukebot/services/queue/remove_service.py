from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import CommandInteraction, Embed
from disnake.ext import commands

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import ResultSet


class RemoveService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction, song: str):
        queue: ResultSet = self.bot.players[interaction.guild.id].queue
        if not (elem := queue.remove(song)):
            raise commands.UserInputError(f"Can't delete item `{song}`")

        e: Embed = embed.basic_message(
            interaction.author,
            content=f"`{elem.title}` have been removed from the queue",
        )
        await interaction.send(embed=e)
