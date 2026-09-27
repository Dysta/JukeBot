from __future__ import annotations

from jukebot.abstract_components import AbstractService
from jukebot.components import Player


class LoopService(AbstractService):
    async def __call__(self, /, guild_id: int, mode: str):
        player: Player = self.bot.players[guild_id]

        old_status = player.loop
        new_status = Player.Loop(mode)
        player.loop = new_status

        return old_status, new_status
