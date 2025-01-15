from __future__ import annotations

from typing import TYPE_CHECKING

from jukebot.abstract_components import AbstractMap
from jukebot.components.player import Player

if TYPE_CHECKING:
    from typing import List


class PlayerSet(AbstractMap[int, Player]):
    _instance = None

    def __new__(cls, bot):
        if cls._instance is None:
            cls._instance = super(PlayerSet, cls).__new__(cls)
            cls.bot = bot
        return cls._instance

    def __getitem__(self, key):
        if not key in self._collection:
            self._collection[key] = Player(self.bot, guild_id=key)
        return self._collection[key]

    def playing(self) -> List[Player]:
        return [p for p in self._collection.values() if p.is_playing]
