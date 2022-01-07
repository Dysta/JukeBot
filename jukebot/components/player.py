import asyncio
import os

from asyncio import Task
from enum import Enum
from typing import Optional

from nextcord import VoiceChannel, VoiceClient
from nextcord.ext.commands import Bot, Context

from jukebot.utils import coro

from .resultset import ResultSet
from .song import Song
from .audio_stream import AudioStream


class Player:
    class State(Enum):
        IDLE = 0
        PLAYING = 1
        PAUSED = 2
        STOPPED = 3
        SKIPPING = 4

    class Loop(Enum):
        DISABLED = 0
        ENABLED = 1

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
        self._voice = await channel.connect()

    async def play(self, song: Song):
        stream = AudioStream(song.stream_url)
        stream.read()

        if self._voice and self._voice.is_playing():
            self._voice.stop()

        self._voice.play(stream, after=self._after)
        self._stream = stream
        self._song = song
        self.state = Player.State.PLAYING

    async def disconnect(self):
        if self._voice:
            await self._voice.disconnect()

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
            print(f"_after {error=}")
        if self.state == Player.State.STOPPED:
            return
        if (
            self._loop == Player.Loop.ENABLED
            and not self.state == Player.State.SKIPPING
        ):
            func = self.play(self.song)
            coro.run_threadsafe(func, self.bot.loop)
            return

        self._stream = None
        self._song = None

        if not self._queue.is_empty():
            func = self.bot.get_cog("Music").play(
                context=self._context,
                query="",
            )
            coro.run_threadsafe(func, self.bot.loop)
        else:
            self.state = Player.State.IDLE

    async def _idle(self) -> None:
        time = float(os.environ["BOT_MAX_IDLE_TIME"])
        await asyncio.sleep(delay=time)

    def _idle_callback(self, task: Task) -> None:
        if not task.cancelled():
            func = self.bot.get_cog("Music").leave(context=self._context)
            asyncio.ensure_future(func, loop=self.bot.loop)

    def _set_idle_task(self) -> None:
        if self._is_inactive() and not self._idle_task:
            task = self.bot.loop.create_task(self._idle())
            task.add_done_callback(self._idle_callback)
            self._idle_task = task
        elif not self._is_inactive() and self._idle_task:
            self._idle_task.cancel()
            self._idle_task = None

    @property
    def stream(self) -> Optional[AudioStream]:
        return self._stream

    @property
    def voice(self) -> Optional[VoiceClient]:
        return self._voice

    @voice.setter
    def voice(self, v: VoiceClient):
        self._voice = v

    @property
    def streaming(self) -> bool:
        return bool(self.stream and self.voice)

    @property
    def playing(self) -> bool:
        return bool(self.stream and self.voice and self.state == Player.State.PLAYING)

    @property
    def connected(self) -> bool:
        return bool(self._voice)

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

    def _is_inactive(self) -> bool:
        return self._state in (
            Player.State.IDLE,
            Player.State.PAUSED,
            Player.State.STOPPED,
        )
