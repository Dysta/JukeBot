from __future__ import annotations

import traceback
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING

from disnake.ext import commands
from loguru import logger

from jukebot.abstract_components.abstract_map import AbstractMap
from jukebot.abstract_components.abstract_service import AbstractService
from jukebot.components import PlayerSet
from jukebot.utils import regex

if TYPE_CHECKING:
    from jukebot.services import ResetService
    from jukebot.services.music import (
        CurrentSongService,
        GrabService,
        JoinService,
        LeaveService,
        LoopService,
        PauseService,
        PlayService,
        ResumeService,
        SkipService,
        StopService,
    )
    from jukebot.services.queue import AddService, ClearService, RemoveService, ShowService, ShuffleService


class ServiceMap(AbstractMap[str, AbstractService]):
    """Typed service attributes, populated by JukeBot.add_service during cog setup."""

    add: AddService
    clear: ClearService
    current_song: CurrentSongService
    grab: GrabService
    join: JoinService
    leave: LeaveService
    loop: LoopService
    pause: PauseService
    play: PlayService
    remove: RemoveService
    reset: ResetService
    resume: ResumeService
    show: ShowService
    shuffle: ShuffleService
    skip: SkipService
    stop: StopService


class JukeBot(commands.InteractionBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = datetime.now()
        self._players: PlayerSet = PlayerSet(self)
        self._services: ServiceMap = ServiceMap()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_error(self, event, *args, **kwargs):
        logger.error(f"{event=}{args}{kwargs}")
        logger.error(f"{''.join(traceback.format_stack())}")

    def add_service(self, service: AbstractService):
        """Add service add a service to the bot. The services are in the services packages.
        When a service is added, you can call it using `bot.services.<service_name>`.
        For example, if your service is called `PlayService`, then you can call it using `bot.services.play`.
        Declare its attribute in ServiceMap as well to enable static type checking and completion.

        Parameters
        ----------
        service : AbstractService
            The service to add. Must implement `AbstractService`!
        """
        name: str = regex.to_snake(service.__class__.__name__).replace("_service", "")
        self.services[name] = service
        setattr(self.services, name, service)

    @property
    def start_time(self):
        return self._start

    @property
    def players(self) -> PlayerSet:
        return self._players

    @property
    def services(self) -> ServiceMap:
        return self._services

    @cached_property
    def members_count(self) -> int:
        return len(set(self.get_all_members()))

    @cached_property
    def guilds_count(self) -> int:
        return len(self.guilds)
