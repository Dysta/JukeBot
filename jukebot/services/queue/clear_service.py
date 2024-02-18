from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import Embed
from disnake.ext import commands

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import Player


class ClearService(AbstractService):
    async def __call__(self):
        player: Player = self.bot.players[self.interaction.guild.id]
        if player.loop == components.Player.Loop.QUEUE:
            raise commands.UserInputError("Can't clear queue when queue loop is enabled")

        player.queue = components.ResultSet.empty()

        e: Embed = embed.basic_message(title="The queue have been cleared.")
        await self.interaction.send(embed=e)
