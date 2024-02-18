from __future__ import annotations

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class LeaveService(AbstractService):
    async def __call__(self):
        # once the bot leave, we destroy is instance from the container
        await self.bot.players.pop(self.interaction.guild.id).disconnect()
        e = embed.basic_message(title="Player disconnected")
        await self.interaction.send(embed=e)
