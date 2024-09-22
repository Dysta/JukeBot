from __future__ import annotations


from jukebot.abstract_components import AbstractService


class ShuffleService(AbstractService):
    async def __call__(self, /, guild_id: int):
        self.bot.players[guild_id].queue.shuffle()
