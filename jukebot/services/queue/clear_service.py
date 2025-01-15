from __future__ import annotations

from typing import TYPE_CHECKING

from disnake.ext import commands

from jukebot import components
from jukebot.abstract_components import AbstractService

if TYPE_CHECKING:
    from jukebot.components import Player


class ClearService(AbstractService):
    async def __call__(self, /, guild_id: int):
        player: Player = self.bot.players[guild_id]
        if player.loop == components.Player.Loop.QUEUE:
            raise commands.UserInputError("Can't clear queue when queue loop is enabled")

        player.queue = components.ResultSet.empty()
