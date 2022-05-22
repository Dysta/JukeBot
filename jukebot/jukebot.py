from __future__ import annotations

import traceback
from datetime import datetime
from functools import cached_property
from typing import List, TypeVar

from disnake.ext import commands
from loguru import logger

from jukebot.abstract_components import AbstractMap
from jukebot.components import Player

CXT = TypeVar("CXT", bound="Context")


class JukeBot(commands.InteractionBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = datetime.now()
        self._players: PlayerCollection = PlayerCollection(self)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_error(self, event, *args, **kwargs):
        logger.error(f"{event=}{args}{kwargs}")
        traceback.print_exc()

    @property
    def start_time(self):
        return self._start

    @property
    def players(self) -> "PlayerCollection":
        return self._players

    @cached_property
    def members_count(self) -> int:
        return len(set(self.get_all_members()))

    @cached_property
    def guilds_count(self) -> int:
        return len(self.guilds)


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

    def playing(self) -> List[Player]:
        return [p for p in self._collection.values() if p.is_playing]
