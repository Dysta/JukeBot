from __future__ import annotations


from jukebot.abstract_components import AbstractService


class ShowService(AbstractService):
    async def __call__(self, /, guild_id: int):
        return self.bot.players[guild_id].queue
