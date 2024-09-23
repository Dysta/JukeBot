from __future__ import annotations

from typing import TYPE_CHECKING


from jukebot import components
from jukebot.abstract_components import AbstractService

if TYPE_CHECKING:
    from jukebot.components import Player


class LoopService(AbstractService):
    async def __call__(self, /, guild_id: int, mode: str):
        # TODO: refactor to use enum str
        player: Player = self.bot.players[guild_id]
        if mode == "song":
            player.loop = components.Player.Loop.SONG
            new_status = "Loop is set to song"
        elif mode == "queue":
            player.loop = components.Player.Loop.QUEUE
            new_status = "Loop is set to queue"
        elif mode == "none":
            player.loop = components.Player.Loop.DISABLED
            new_status = "Loop is disabled"

        return new_status
