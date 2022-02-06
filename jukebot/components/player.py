import asyncio
import os

from asyncio import Task
from enum import IntEnum
from typing import Optional

from loguru import logger
from nextcord import VoiceChannel, VoiceClient
from nextcord.ext.commands import Bot, Context

from jukebot.utils import coro

from .resultset import ResultSet
from .song import Song
from .audio_stream import AudioStream


class Player:
    class State(IntEnum):
        IDLE = 0
        PLAYING = 1
        PAUSED = 2
        STOPPED = 3
        SKIPPING = 4
        DISCONNECTING = 5

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
        ENABLED = 1

        @property
        def is_enabled(self) -> bool:
            return self == Player.Loop.ENABLED

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

        self._voice: Optional[VoiceClient] = None
        self._stream: Optional[AudioStream] = None
        self._context: Optional[Context] = None
        self._song: Optional[Song] = None
        self._queue: ResultSet = ResultSet.empty()
        self._state: Player.State = Player.State.IDLE
        self._idle_task: Optional[Task] = None
        self._loop: Player.Loop = Player.Loop.DISABLED

    async def join(self, channel: VoiceChannel):
        self._voice = await channel.connect(timeout=3.0)

    async def play(self, song: Song, is_tts: bool = False):
        if is_tts:
            stream = AudioStream(song.stream_url, before_options="", options="")
        else:
            stream = AudioStream(song.stream_url)
        stream.read()

        if self._voice and self._voice.is_playing():
            self._voice.stop()

        self._voice.play(
            stream,
            after=lambda e: self._after(
                error=e, is_tts=is_tts, filename=song.stream_url
            ),
        )
        self._stream = stream
        self._song = song
        self.state = Player.State.PLAYING

    async def play_tts(self, filename: str):
        stream = AudioStream(filename, before_options=None, options=None)
        stream.read()

        if self._voice and self._voice.is_playing():
            self._voice.stop()

        self._voice.play(stream, after=lambda e: os.remove(filename))
        self._stream = stream
        # self._song = song
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

    def _after(self, error, is_tts: bool = False, filename: str = None):
        if is_tts:
            os.remove(filename)
        if error:
            logger.opt(lazy=True).error(error)
            return
        if self.state.is_leaving:
            return
        if self._loop.is_enabled and not self.state.is_skipping:
            func = self.play(self.song)
            coro.run_threadsafe(func, self.bot.loop)
            return

        self._stream = None
        self._song = None

        if not self._queue.is_empty():
            music_cog = self.bot.get_cog("Music")
            func = self.context.invoke(music_cog.play, query="")
            coro.run_threadsafe(func, self.bot.loop)
        else:
            self.state = Player.State.IDLE

    def _idle_callback(self) -> None:
        if not self._idle_task.cancelled():
            music_cog = self.bot.get_cog("Music")
            func = self.context.invoke(music_cog.leave)
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
    def context(self) -> Optional[Context]:
        return self._context

    @context.setter
    def context(self, c: Context) -> None:
        self._context = c

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new: State) -> None:
        self._state = new
        self._set_idle_task()

    @property
    def loop(self) -> "Player.Loop":
        return self._loop

    @loop.setter
    def loop(self, lp: "Player.Loop") -> None:
        self._loop = lp
