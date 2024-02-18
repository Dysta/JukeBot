from __future__ import annotations

from typing import Optional
from urllib import parse

from disnake import CommandInteraction, Embed
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from jukebot.components.requests import ShazamRequest
from jukebot.exceptions import QueryFailed
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
from jukebot.utils import aioweb, checks, embed, regex


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.user_is_connected)
    async def play(self, inter: CommandInteraction, query: str, top: Optional[bool] = False):
        """Play music from URL or search

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        query : str
            The URL or search to play
        top : Optional[bool], optional
            Put the requested song at the top of the queue, by default False
        """
        with PlayService(self.bot) as ps:
            await ps(interaction=inter, query=query, top=top)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def leave(self, inter: CommandInteraction):
        """Disconnect the bot from the current connected voice channel.

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with LeaveService(self.bot) as ls:
            await ls(interaction=inter)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_is_playing)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def stop(self, inter: CommandInteraction):
        """Stop and skip current music without disconnecting bot from voice channel

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with StopService(self.bot) as ss:
            await ss(interaction=inter)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_is_playing)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def pause(self, inter: CommandInteraction):
        """Pause the current music without skipping it

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with PauseService(self.bot) as ps:
            await ps(interaction=inter)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_is_not_playing)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def resume(self, inter: CommandInteraction):
        """Resumes the current or the next music

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with ResumeService(self.bot) as rs:
            await rs(interaction=inter)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def current(self, inter: CommandInteraction):
        """Shows the music currently playing and its progress

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with CurrentSongService(self.bot) as css:
            await css(inter)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.user_is_connected)
    @commands.check(checks.bot_is_not_connected)
    async def join(self, inter: CommandInteraction):
        """Connect the bot to the voice channel you are in

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with JoinService(self.bot) as js:
            await js(interaction=inter)

    @commands.slash_command()
    @commands.cooldown(3, 10.0, BucketType.user)
    @commands.check(checks.bot_is_streaming)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def skip(self, inter: CommandInteraction):
        """Skips to the next music in the queue. Stop the music if the queue is empty

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with SkipService(self.bot) as ss:
            await ss(interaction=inter)

    @commands.slash_command()
    @commands.check(checks.bot_is_playing)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.user)
    async def grab(self, inter: CommandInteraction):
        """Similar to the current command but sends the message in DM

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with GrabService(self.bot) as gs:
            await gs(interaction=inter)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def loop(
        self,
        inter: CommandInteraction,
        mode: commands.option_enum(["song", "queue", "none"]),
    ):
        """
        Allow user to enable or disable the looping of a song or queue.

        Parameters
        ----------
        inter: The interaction
        mode: The loop mode
                - song (loop the current song)
                - queue (loop the current queue)
                - none (disable looping)
        """
        with LoopService(self.bot) as lp:
            await lp(interaction=inter, mode=mode)

    @commands.slash_command()
    @commands.cooldown(1, 15.0, BucketType.guild)
    @commands.max_concurrency(1, BucketType.guild)
    async def find(self, inter: CommandInteraction, url: str):
        """
        Parses the media at the given URL and returns the music used in it

        Parameters
        ----------
        inter: The interaction
        url: The url of the media to analyze
        """
        if not regex.is_url(url):
            raise commands.UserInputError("Query must be an url to a media")

        await inter.response.defer()

        async with ShazamRequest(url) as req:
            await req.execute()

        if not req.success:
            raise QueryFailed(f"No music found for this media..", query="", full_query=url)

        e: Embed = embed.music_found_message(req.result)
        await inter.edit_original_message(embed=e)

    @commands.slash_command()
    @commands.cooldown(1, 10.0, BucketType.guild)
    @commands.max_concurrency(1, BucketType.guild)
    async def share(self, inter: CommandInteraction, url: str):
        """
        Returns all streaming platforms available for the given media

        Parameters
        ----------
        inter: The inter
        url: The url of the music/album to share
        """
        if not regex.is_url(url):
            raise commands.UserInputError("You must provide an URL.")

        await inter.response.defer()

        base_url = "https://api.song.link/v1-alpha.1/links?url=%s"
        code, data = await aioweb.cached_query(base_url % parse.quote(url))

        if code != 200:
            raise commands.UserInputError("The URL didn't return anything")

        content = " | ".join(
            f"[{k.capitalize()}]({v['url']})" for k, v in sorted(data["linksByPlatform"].items(), key=lambda x: x)
        )
        title: str = data["entitiesByUniqueId"][data["entityUniqueId"]].get("title", "Unknown title")
        artist: str = data["entitiesByUniqueId"][data["entityUniqueId"]].get("artistName", "Unknown artist")
        img: str = data["entitiesByUniqueId"][data["entityUniqueId"]].get("thumbnailUrl", "")
        e: Embed = embed.share_message(
            inter.author,
            title=f"{artist} - {title}",
            content=content,
            url=data["pageUrl"],
            img=img,
        )
        await inter.edit_original_message(embed=e)


def setup(bot):
    bot.add_cog(Music(bot))
