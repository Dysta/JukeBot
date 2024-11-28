from __future__ import annotations


from jukebot.abstract_components import AbstractService


class LeaveService(AbstractService):
    async def __call__(self, /, guild_id: int):
        # once the bot leave, we destroy is instance from the container
        await self.bot.players.pop(guild_id).disconnect()
