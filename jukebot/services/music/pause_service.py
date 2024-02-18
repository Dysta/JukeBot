from __future__ import annotations

from typing import Optional


from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class PauseService(AbstractService):
    async def __call__(self, /, silent: Optional[bool] = False):
        self.bot.players[self.interaction.guild.id].pause()
        if not silent:
            e = embed.basic_message(title="Player paused")
            await self.interaction.send(embed=e)
