import json
from threading import Lock

import nextcord
import os
from datetime import datetime

from nextcord import Guild
from nextcord.ext import commands, tasks

from jukebot.abstract_components import AbstractCollection


class JukeBot(commands.Bot, nextcord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._activity = nextcord.Game(f"{os.environ['BOT_PREFIX']}help")
        self._start = None
        self._prefixes: PrefixCollection = PrefixCollection.load()
        self._save_prefix.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        self._start = datetime.now()
        await self.change_presence(
            status=nextcord.Status.online, activity=self._activity
        )

    async def close(self):
        self._prefixes.export()
        await super().close()

    async def on_error(self, event, *args, **kwargs):
        print(f"{event=}{args}{kwargs}")

    async def on_guild_join(self, guild: Guild):
        self._prefixes[guild.id] = os.environ["BOT_PREFIX"]

    async def on_guild_remove(self, guild):
        del self._prefixes[guild.id]

    @tasks.loop(minutes=30)
    async def _save_prefix(self):
        self._prefixes.export()

    @_save_prefix.before_loop
    async def before_save(self):
        await self.wait_until_ready()

    @property
    def start_time(self):
        return self._start

    @property
    def prefixes(self) -> "PrefixCollection":
        return self._prefixes


class PrefixCollection(AbstractCollection[str, str]):
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PrefixCollection, cls).__new__(cls)
        return cls._instance

    def export(self):
        with open("data/prefixes.json", "w") as f:
            json.dump(self.__dict__, f)

    @staticmethod
    def load():
        with open("data/prefixes.json", "r") as f:
            data = json.load(f)
        col = PrefixCollection()
        col.__dict__ = data
        return col
