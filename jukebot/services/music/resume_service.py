from __future__ import annotations

from typing import TYPE_CHECKING


from jukebot.abstract_components import AbstractService


if TYPE_CHECKING:
    from jukebot.components import Player


class ResumeService(AbstractService):
    async def __call__(self, /, guild_id: int):
        player: Player = self.bot.players[guild_id]
        if player.is_paused:
            player.resume()
            return True

        return False
