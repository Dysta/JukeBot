import asyncio

import os

from datetime import datetime

from nextcord import Guild
from nextcord.ext import commands

from jukebot.abstract_components import AbstractMongoDB


class JukeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = datetime.now()
        self._prefixes: PrefixDB = PrefixDB(
            url=os.environ["MONGO_DB_URI"], database="jukebot", collection="prefixes"
        )

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def on_error(self, event, *args, **kwargs):
        print(f"{event=}{args}{kwargs}")

    async def on_guild_join(self, guild: Guild):
        await self._prefixes.set_item(guild.id, os.environ["BOT_PREFIX"])

    async def on_guild_remove(self, guild):
        await self._prefixes.del_item(guild.id)

    @property
    def start_time(self):
        return self._start

    @property
    def prefixes(self) -> "PrefixDB":
        return self._prefixes


class PrefixDB(AbstractMongoDB):
    async def contain(self, guild_id: int) -> bool:
        item = {"guild_id": guild_id}
        res = await self._collection.find_one(item)
        return bool(res)

    async def get_item(self, guild_id: int) -> str:
        item = {"guild_id": guild_id}
        res = await self._collection.find_one(item)
        return res["prefix"]

    async def set_item(self, guild_id: int, prefix: str) -> None:
        key = {"guild_id": guild_id}
        value = {"$set": {"prefix": prefix}}
        asyncio.ensure_future(self._collection.update_one(key, value, upsert=True))

    async def del_item(self, guild_id: int) -> None:
        item = {"guild_id": guild_id}
        asyncio.ensure_future(self._collection.delete_one(item))
