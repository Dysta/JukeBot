from __future__ import annotations


from jukebot.abstract_components import AbstractService
from jukebot.utils import embed


class StopService(AbstractService):
    async def __call__(self):
        self.bot.players[self.interaction.guild.id].stop()
        e = embed.basic_message(title="Player stopped")
        await self.interaction.send(embed=e)
