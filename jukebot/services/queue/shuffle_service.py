from __future__ import annotations

from disnake import Embed

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class ShuffleService(AbstractService):
    async def __call__(self):
        self.bot.players[self.interaction.guild.id].queue.shuffle()
        e: Embed = embed.basic_message(title="Queue shuffled.")
        await self.interaction.send(embed=e)
