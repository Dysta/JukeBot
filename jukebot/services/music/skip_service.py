from __future__ import annotations

from typing import Optional


from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class SkipService(AbstractService):
    async def __call__(self, /, silent: Optional[bool] = False):
        self.bot.players[self.interaction.guild.id].skip()
        if not silent:
            e: embed = embed.basic_message(title="Skipped !")
            await self.interaction.send(embed=e)
