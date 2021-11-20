import asyncio
import discord
import platform
import sys

from typing import Optional

from discord import VoiceClient, VoiceChannel
from discord.ext.commands import Context, Bot

from .song import Song
from .audio_stream import AudioStream
from collections import abc
from enum import Enum


class Player:
    class State(Enum):
        IDLE = 0
        PLAYING = 1
        PAUSED = 2

    def __init__(self, bot: Bot, guild_id: int):
        self.bot: Bot = bot
        self.guild_id: int = guild_id

        self._voice: Optional[VoiceClient] = None
        self._current: Optional[AudioStream] = None
        self._song: Optional[Song] = None
        self._next = asyncio.Event()
        self._queue = asyncio.Queue()

        self._state: Player.State = Player.State.IDLE

    async def join(self, channel: VoiceChannel):
        if self._voice is None or not self._voice.is_connected():
            try:
                self._voice = await channel.connect()
            except asyncio.TimeoutError:
                return "Could not connect to the voice channel in time."
            except discord.ClientException:
                return "Already connected to a voice channel."
        if self._voice.channel.id != channel.id:
            await self._voice.move_to(channel)
        return True

    async def play(self, ctx: Context, song):

        try:
            audio = discord.FFmpegPCMAudio(
                song.stream_url,
                executable=_PlayerOption.FFMPEG_EXECUTABLE[platform.system()],
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

        if self._voice and self._voice.is_playing():
            self._voice.stop()

        self._voice.play(player)
        self._current = player
        self._song = song

    async def disconnect(self):
        if self._voice:
            await self._voice.disconnect()

    def stop(self):
        if self._voice:
            self._voice.stop()

    def pause(self):
        if self._voice:
            self._voice.pause()

    def resume(self):
        if self._voice:
            self._voice.resume()

    @property
    def current(self) -> Optional[AudioStream]:
        return self._current

    @property
    def voice(self) -> Optional[VoiceClient]:
        return self._voice

    @voice.setter
    def voice(self, v: VoiceClient):
        self._voice = v

    @property
    def playing(self) -> bool:
        return bool(self.current and self.voice)

    @property
    def song(self):
        return self._song


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
    FFMPEG_EXECUTABLE = {"Linux": "./bin/ffmpeg", "Windows": "./bin/ffmpeg.exe"}

    FFMPEG_BEFORE_OPTIONS = " ".join(
        ["-reconnect 1", "-reconnect_streamed 1", "-reconnect_delay_max 3", "-nostdin"]
    )

    FFMPEG_OPTIONS = "-vn"
