from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from jukebot.abstract_components import AbstractMap
from jukebot.components.player import Player

if TYPE_CHECKING:
    from jukebot import JukeBot


class PlayerSet(AbstractMap[int, Player]):
    bot: ClassVar[JukeBot]
    _instance = None

    def __new__(cls, bot: JukeBot):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.bot = bot
        return cls._instance

    def __getitem__(self, k: int) -> Player:
        if not k in self._collection:
            self._collection[k] = Player(self.bot, guild_id=k)
        return self._collection[k]

    def playing(self) -> list[Player]:
        return [p for p in self._collection.values() if p.is_playing]
