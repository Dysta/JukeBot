from __future__ import annotations

import asyncio
import os
from asyncio import Task
from enum import IntEnum, auto
from typing import Optional

from disnake import CommandInteraction, VoiceChannel, VoiceClient
from disnake.ext.commands import Bot
from loguru import logger

from jukebot.components.audio_stream import AudioStream
from jukebot.components.requests import StreamRequest
from jukebot.components.resultset import ResultSet
from jukebot.components.song import Song
from jukebot.services.music import LeaveService, PlayService
from jukebot.services.queue import AddService
from jukebot.utils import coro


class Player:
    class State(IntEnum):
        IDLE = auto()
        PLAYING = auto()
        PAUSED = auto()
        STOPPED = auto()
        SKIPPING = auto()
        DISCONNECTING = auto()

        @property
        def is_playing(self) -> bool:
            return self == Player.State.PLAYING

        @property
        def is_paused(self) -> bool:
            return self == Player.State.PAUSED

        @property
        def is_stopped(self) -> bool:
            return self == Player.State.STOPPED

        @property
        def is_skipping(self) -> bool:
            return self == Player.State.SKIPPING

        @property
        def is_inactive(self) -> bool:
            return self in [
                Player.State.IDLE,
                Player.State.PAUSED,
                Player.State.STOPPED,
            ]

        @property
        def is_leaving(self) -> bool:
            return self in [Player.State.STOPPED, Player.State.DISCONNECTING]

    class Loop(IntEnum):
        DISABLED = 0
        SONG = 1
        QUEUE = 2

        @property
        def is_song_loop(self) -> bool:
            return self == Player.Loop.SONG

        @property
        def is_queue_loop(self) -> bool:
            return self == Player.Loop.QUEUE

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

        self._voice: Optional[VoiceClient] = None
        self._stream: Optional[AudioStream] = None
        self._inter: Optional[CommandInteraction] = None
        self._song: Optional[Song] = None
        self._queue: ResultSet = ResultSet.empty()
        self._state: Player.State = Player.State.IDLE
        self._idle_task: Optional[Task] = None
        self._loop: Player.Loop = Player.Loop.DISABLED

    async def join(self, channel: VoiceChannel):
        self._voice = await channel.connect(timeout=2.0)
        self.state = Player.State.IDLE

    async def play(self, song: Song, replay: bool = False):
        if replay:
            # ? we must requery the song to refresh the stream URL
            # ? some website can invalidate the stream URL after some times
            author = song.requester
            async with StreamRequest(song.web_url) as req:
                await req.execute()

            song: Song = Song(req.result)
            song.requester = author

        if self._voice and self._voice.is_playing():
            self._voice.stop()

        stream = AudioStream(song.stream_url)

        self._voice.play(stream, after=self._after)
        self._stream = stream
        self._song = song
        self.state = Player.State.PLAYING

    async def disconnect(self, force=False):
        if self._voice:
            self.state = Player.State.DISCONNECTING
            await self._voice.disconnect(force=force)

    def skip(self):
        if self._voice:
            self.state = Player.State.SKIPPING
            self._voice.stop()

    def stop(self):
        if self._voice:
            self.state = Player.State.STOPPED
            self._voice.stop()

    def pause(self):
        if self._voice:
            self.state = Player.State.PAUSED
            self._voice.pause()

    def resume(self):
        if self._voice:
            self.state = Player.State.PLAYING
            self._voice.resume()

    def _after(self, error):
        if error:
            logger.opt(lazy=True).error(error)
            self.state = Player.State.IDLE
            return

        if self.state.is_leaving:
            return

        if self._loop.is_song_loop and not self.state.is_skipping:
            func = self.play(self.song, replay=True)
            coro.run_threadsafe(func, loop=self.bot.loop)
            return

        if self._loop.is_queue_loop:
            with AddService(self.bot) as ad:
                func = ad(interaction=self.interaction, query=self.song.web_url, silent=True)
            asyncio.ensure_future(func, loop=self.bot.loop)

        self._stream = None
        self._song = None

        if not self._queue.is_empty():
            with PlayService(self.bot) as ps:
                func = ps(interaction=self.interaction, query="")
            coro.run_threadsafe(func, self.bot.loop)
            return

        self.state = Player.State.IDLE

    def _idle_callback(self) -> None:
        if not self._idle_task.cancelled():
            with LeaveService(self.bot) as ls:
                func = ls(interaction=self.interaction)
            asyncio.ensure_future(func, loop=self.bot.loop)

    def _set_idle_task(self) -> None:
        if self.state.is_inactive and not self._idle_task:
            self._idle_task = self.bot.loop.call_later(
                delay=float(os.environ["BOT_MAX_IDLE_TIME"]),
                callback=self._idle_callback,
            )
        elif not self.state.is_inactive and self._idle_task:
            self._idle_task.cancel()
            self._idle_task = None

    @property
    def is_streaming(self) -> bool:
        return self.is_connected and bool(self.stream)

    @property
    def is_playing(self) -> bool:
        return self.is_streaming and self.state.is_playing

    @property
    def is_paused(self) -> bool:
        return self.is_streaming and self.state.is_paused

    @property
    def is_connected(self) -> bool:
        return bool(self._voice)

    @property
    def stream(self) -> Optional[AudioStream]:
        return self._stream

    @property
    def voice(self) -> Optional[VoiceClient]:
        return self._voice

    @property
    def song(self) -> Optional[Song]:
        return self._song

    @property
    def queue(self) -> ResultSet:
        return self._queue

    @queue.setter
    def queue(self, q) -> None:
        self._queue = q

    @property
    def interaction(self) -> Optional[CommandInteraction]:
        return self._inter

    @interaction.setter
    def interaction(self, c: CommandInteraction) -> None:
        self._inter = c

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new: State) -> None:
        self._state = new
        self._set_idle_task()

    @property
    def loop(self) -> Player.Loop:
        return self._loop

    @loop.setter
    def loop(self, lp: Player.Loop) -> None:
        self._loop = lp
