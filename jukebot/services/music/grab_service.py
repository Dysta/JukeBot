from __future__ import annotations

from typing import TYPE_CHECKING


from jukebot.abstract_components import AbstractService

if TYPE_CHECKING:
    from jukebot.components import AudioStream, Player, Song


class GrabService(AbstractService):
    async def __call__(self, /, guild_id: int):
        player: Player = self.bot.players[guild_id]
        stream: AudioStream = player.stream
        song: Song = player.song

        return song, stream
