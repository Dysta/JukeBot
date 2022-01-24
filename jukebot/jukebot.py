import asyncio
import os

from datetime import datetime
from functools import cached_property
from typing import TypeVar

from nextcord import Guild, Message
from nextcord.ext import commands

from loguru import logger

from jukebot.abstract_components import AbstractMongoDB, AbstractMap
from jukebot.components import Player, CustomContext

CXT = TypeVar("CXT", bound="Context")


class JukeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = datetime.now()
        self._prefixes: PrefixDB = PrefixDB(
            url=os.environ["MONGO_DB_URI"],
            database=os.environ["MONGO_DB_DATABASE"],
            collection=os.environ["MONGO_DB_COLLECTION"],
        )
        self._players: PlayerCollection = PlayerCollection(self)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_error(self, event, *args, **kwargs):
        logger.error(f"{event=}{args}{kwargs}")

    async def on_guild_join(self, guild: Guild):
        await self._prefixes.set_item(guild.id, os.environ["BOT_PREFIX"])

    async def on_guild_remove(self, guild):
        await self._prefixes.del_item(guild.id)

    async def get_context(self, message: Message, *, cls=CustomContext) -> CXT:
        return await super().get_context(message, cls=cls)

    @property
    def start_time(self):
        return self._start

    @property
    def prefixes(self) -> "PrefixDB":
        return self._prefixes

    @property
    def players(self) -> "PlayerCollection":
        return self._players

    @cached_property
    def members_count(self) -> int:
        return len(set(self.get_all_members()))

    @cached_property
    def guilds_count(self) -> int:
        return len(self.guilds)


class PrefixDB(AbstractMongoDB):
    async def contains(self, guild_id: int) -> bool:
        item = {"guild_id": guild_id}
        res = await self._collection.find_one(item)
        return bool(res)

    async def get_item(self, guild_id: int) -> str:
        item = {"guild_id": guild_id}
        res = await self._collection.find_one(item)
        return res["prefix"] if res else None

    async def set_item(self, guild_id: int, prefix: str) -> None:
        key = {"guild_id": guild_id}
        value = {"$set": {"prefix": prefix}}
        asyncio.ensure_future(self._collection.update_one(key, value, upsert=True))

    async def del_item(self, guild_id: int) -> None:
        item = {"guild_id": guild_id}
        asyncio.ensure_future(self._collection.delete_one(item))


class PlayerCollection(AbstractMap[int, Player]):
    _instance = None

    def __new__(cls, bot):
        if cls._instance is None:
            cls._instance = super(PlayerCollection, cls).__new__(cls)
            cls.bot = bot
        return cls._instance

    def __getitem__(self, key):
        if not key in self._collection:
            self._collection[key] = Player(self.bot)
        return self._collection[key]
