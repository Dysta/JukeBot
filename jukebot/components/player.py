import asyncio
import nextcord
import platform
import sys

from enum import Enum
from threading import Lock
from typing import Optional

from nextcord import VoiceChannel, VoiceClient
from nextcord.ext.commands import Bot, Context

from ..abstract_components import AbstractCollection
from .result import Result
from .resultset import ResultSet
from .song import Song
from .audio_stream import AudioStream


class Player:
    class State(Enum):
        IDLE = 0
        PLAYING = 1
        PAUSED = 2
        STOPPED = 3

    def __init__(self, bot: Bot, guild_id: int):
        self.bot: Bot = bot
        self.guild_id: int = guild_id

        self._voice: Optional[VoiceClient] = None
        self._stream: Optional[AudioStream] = None
        self._context: Optional[Context] = None
        self._song: Optional[Song] = None
        self._queue: ResultSet = ResultSet.empty()

        self._state: Player.State = Player.State.IDLE

    async def join(self, channel: VoiceChannel):
        if not self._voice or not self._voice.is_connected():
            try:
                self._voice = await channel.connect()
            except asyncio.TimeoutError:
                return "Could not connect to the voice channel in time."
            except nextcord.ClientException:
                return "Already connected to a voice channel."
        if self._voice.channel.id != channel.id:
            await self._voice.move_to(channel)
        return True

    async def play(self, song: Song):
        try:
            audio = nextcord.FFmpegPCMAudio(
                song.stream_url,
                executable=_PlayerOption.FFMPEG_EXECUTABLE[platform.system()],
                pipe=False,
                stderr=sys.stdout,  # None,  # subprocess.PIPE
                before_options=_PlayerOption.FFMPEG_BEFORE_OPTIONS,  # "-nostdin",
                options=_PlayerOption.FFMPEG_OPTIONS,
            )
        except nextcord.ClientException:
            print("_play_now", "The subprocess failed to be created")
            return

        stream = AudioStream(audio)
        stream.read()

        if self._voice and self._voice.is_playing():
            self._voice.stop()

        self._voice.play(stream, after=self._after)
        self._stream = stream
        self._song = song
        self._state = Player.State.PLAYING

    def _after(self, error):
        if error:
            print(f"_after {error=}")
        if self._state == Player.State.STOPPED:
            return

        self._state = Player.State.IDLE
        self._stream = None
        self._song = None

        if len(self._queue):
            req: Result = self._queue.get()
            func = self.bot.get_cog("Music").play(
                context=self._context, author=req.author, force=True, query=req.web_url
            )
            fut = asyncio.run_coroutine_threadsafe(func, self.bot.loop)
            fut.result()

    async def disconnect(self):
        if self._voice:
            self._state = Player.State.STOPPED
            await self._voice.disconnect()

    def stop(self):
        if self._voice:
            self._state = Player.State.IDLE
            self._voice.stop()

    def pause(self):
        if self._voice:
            self._state = Player.State.PAUSED
            self._voice.pause()

    def resume(self):
        if self._voice:
            self._state = Player.State.PLAYING
            self._voice.resume()

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
    def playing(self) -> bool:
        return bool(self.stream and self.voice and self._state == Player.State.PLAYING)

    @property
    def connected(self) -> bool:
        return bool(self._voice)

    @property
    def song(self) -> Optional[Song]:
        return self._song

    @property
    def queue(self) -> ResultSet:
        return self._queue

    @property
    def context(self) -> Optional[Context]:
        return self._context

    @context.setter
    def context(self, c: Context) -> None:
        self._context = c


class PlayerCollection(AbstractCollection[int, Player]):
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, bot):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PlayerCollection, cls).__new__(cls)
                cls.bot = bot
        return cls._instance

    def __getitem__(self, key):
        if not key in self._collection:
            self._collection[key] = Player(self.bot, key)
        return self._collection[key]


class _PlayerOption:
    FFMPEG_EXECUTABLE = {"Linux": "./bin/ffmpeg", "Windows": "./bin/ffmpeg.exe"}

    FFMPEG_BEFORE_OPTIONS = " ".join(
        ["-reconnect 1", "-reconnect_streamed 1", "-reconnect_delay_max 3", "-nostdin"]
    )

    FFMPEG_OPTIONS = "-vn"
