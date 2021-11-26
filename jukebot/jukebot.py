import json

import aiofiles
import nextcord
import os
from datetime import datetime

from nextcord import Guild
from nextcord.ext import commands

from jukebot.abstract_components import AbstractCollection


class JukeBot(commands.Bot, nextcord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._activity = nextcord.Game(f"{os.environ['BOT_PREFIX']}help")
        self._start = None
        self._prefixes: PrefixCollection = PrefixCollection.load()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        self._start = datetime.now()
        await self.change_presence(
            status=nextcord.Status.online, activity=self._activity
        )

    async def close(self):
        await self._prefixes.export()
        await super().close()

    async def on_error(self, event, *args, **kwargs):
        print(f"{event=}{args}{kwargs}")

    async def on_guild_join(self, guild: Guild):
        await self.set_prefix_for(guild.id, os.environ["BOT_PREFIX"])

    async def on_guild_remove(self, guild):
        del self._prefixes[guild.id]
        await self._prefixes.export()

    async def set_prefix_for(self, guild_id, prefix):
        self._prefixes[guild_id] = prefix
        await self._prefixes.export()

    @property
    def start_time(self):
        return self._start

    @property
    def prefixes(self) -> "PrefixCollection":
        return self._prefixes


class PrefixCollection(AbstractCollection[str, str]):
    _instance = None
    _filename = "data/prefixes.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrefixCollection, cls).__new__(cls)
        return cls._instance

    async def export(self):
        async with aiofiles.open(PrefixCollection._filename, "w") as f:
            data = json.dumps(self.__dict__)
            await f.write(data)

    @staticmethod
    def load():
        if not os.path.exists(PrefixCollection._filename):
            data = {}
        else:
            with open(PrefixCollection._filename, "r") as f:
                data = json.load(f)
        col = PrefixCollection()
        col.__dict__ = data
        return col

    def __setitem__(self, key: int, value: str):
        super().__setitem__(str(key), value)

    def __getitem__(self, key: int) -> str:
        return super().__getitem__(str(key))

    def __delitem__(self, key: int) -> None:
        super().__delitem__(str(key))
