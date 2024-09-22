from __future__ import annotations

from typing import TYPE_CHECKING

from disnake.ext import commands

from jukebot.abstract_components import AbstractService

if TYPE_CHECKING:
    from jukebot.components import ResultSet


class RemoveService(AbstractService):
    async def __call__(self, /, guild_id: int, song: str):
        queue: ResultSet = self.bot.players[guild_id].queue
        if not (elem := queue.remove(song)):
            raise commands.UserInputError(f"Can't delete song `{song}`. Not in playlist.")

        return elem
