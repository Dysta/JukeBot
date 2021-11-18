import asyncio
import discord
import sys

from .audio_stream import AudioStream
from collections import abc
from enum import Enum


class Player:
    class State(Enum):
        IDLE = 0
        PLAYING = 1
        PAUSED = 2

    def __init__(self, bot, guild_id: int):
        self.bot = bot
        self.guild_id = guild_id

        self.voice = None
        self._current = None
        self._next = asyncio.Event()
        self._queue = asyncio.Queue()

        self._state = Player.State.IDLE

    async def join(self, channel):
        if self.voice is None or not self.voice.is_connected():
            try:
                self.voice = await channel.connect()
            except asyncio.TimeoutError:
                return "Could not connect to the voice channel in time."
            except discord.ClientException:
                return "Already connected to a voice channel."
        if self.voice.channel.id != channel.id:
            await self.voice.move_to(channel)
        return True

    async def play(self, ctx, req):

        try:
            audio = discord.FFmpegPCMAudio(
                req.stream_url,
                executable=_PlayerOption.FFMPEG_EXECUTABLE,
                pipe=False,
                stderr=sys.stdout,  # None,  # subprocess.PIPE
                before_options=_PlayerOption.FFMPEG_BEFORE_OPTIONS,  # "-nostdin",
                options=_PlayerOption.FFMPEG_OPTIONS,
            )
        except discord.ClientException:
            print("_play_now", "The subprocess failed to be created")
            return

        player = AudioStream(audio)
        player.read()

        await self.join(ctx.message.author.voice.channel)

        if self.voice and self.voice.is_playing():
            self.voice.stop()

        self.voice.play(player)
        self._current = player

    async def disconnect(self):
        if self.voice:
            await self.voice.disconnect()

    def stop(self):
        if self.voice:
            self.voice.stop()

    def pause(self):
        if self.voice:
            self.voice.pause()

    def resume(self):
        if self.voice:
            self.voice.resume()

    @property
    def current(self):
        return self._current

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, v):
        self._voice = v

    @property
    def playing(self):
        return self.current and self.voice


class PlayerCollection(abc.MutableMapping):
    _instance = None

    def __new__(cls, bot):
        if cls._instance is None:
            cls._instance = super(PlayerCollection, cls).__new__(cls)
            cls.bot = bot
        return cls._instance

    def __contains__(self, key):
        return key in self.__dict__.keys()

    def __getitem__(self, key):
        if not key in self.__dict__:
            self.__dict__[key] = Player(self.bot, key)
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        for p in self.__dict__:
            yield p

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class _PlayerOption:
    FFMPEG_EXECUTABLE = "./bin/ffmpeg.exe"

    FFMPEG_BEFORE_OPTIONS = " ".join(
        ["-reconnect 1", "-reconnect_streamed 1", "-reconnect_delay_max 3", "-nostdin"]
    )

    FFMPEG_OPTIONS = "-vn"
