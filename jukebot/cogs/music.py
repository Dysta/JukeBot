from __future__ import annotations

from typing import Optional
from urllib import parse

from disnake import CommandInteraction, Embed
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from jukebot.checks import voice
from jukebot.components import ShazamQuery
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
from jukebot.utils import aioweb, embed, regex


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.user_is_connected)
    async def play(
        self, inter: CommandInteraction, query: str, top: Optional[bool] = False
    ):
        """
        Play a music from the provided URL or a query
        Parameters
        ----------
        inter: The interaction
        query: The URL or query to play
        top: Put the requested song at the top of the queue

        Returns
        -------

        """
        with PlayService(self.bot) as ps:
            await ps(interaction=inter, query=query, top=top)

    @commands.slash_command(
        description="Disconnect the bot from the current connected voice channel.",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def leave(self, inter: CommandInteraction):
        with LeaveService(self.bot) as ls:
            await ls(interaction=inter)

    @commands.slash_command(
        description="Stop the current music from the bot without disconnect him.",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_is_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def stop(self, inter: CommandInteraction):
        with StopService(self.bot) as ss:
            await ss(interaction=inter)

    @commands.slash_command(
        description="Pause the current music from the bot without stop it.",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_is_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def pause(self, inter: CommandInteraction):
        with PauseService(self.bot) as ps:
            await ps(interaction=inter)

    @commands.slash_command(
        description="Resume the current music",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_is_not_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def resume(self, inter: CommandInteraction):
        with ResumeService(self.bot) as rs:
            await rs(interaction=inter)

    @commands.slash_command(
        description="Display the current music and the progression from the bot.",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def current(self, inter: CommandInteraction):
        with CurrentSongService(self.bot) as css:
            await css(inter)

    @commands.slash_command(
        description="Connect the bot to your current voice channel",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.user_is_connected)
    @commands.check(voice.bot_is_not_connected)
    async def join(self, inter: CommandInteraction):
        with JoinService(self.bot) as js:
            await js(interaction=inter)

    @commands.slash_command(
        description="Skip the current song.",
    )
    @commands.cooldown(3, 10.0, BucketType.user)
    @commands.check(voice.bot_is_streaming)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def skip(self, inter: CommandInteraction):
        with SkipService(self.bot) as ss:
            await ss(interaction=inter)

    @commands.slash_command(
        description="Send the current song in your DM to save it.",
    )
    @commands.check(voice.bot_is_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.user)
    async def grab(self, inter: CommandInteraction):
        with GrabService(self.bot) as gs:
            await gs(interaction=inter)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.user_is_connected)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.bot_and_user_in_same_channel)
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

        Returns
        -------

        """
        with LoopService(self.bot) as lp:
            await lp(interaction=inter, mode=mode)

    @commands.slash_command()
    @commands.cooldown(1, 15.0, BucketType.guild)
    @commands.max_concurrency(1, BucketType.guild)
    async def find(self, inter: CommandInteraction, url: str):
        """
        Shazam the song at the given url. It take the 20 first seconds of the media then Shazam it.
        Parameters
        ----------
        inter: The interaction
        url: The url of the media to analyze

        Returns
        -------

        """
        if not regex.is_url(url):
            raise commands.UserInputError("Query must be an url to a media")

        await inter.response.defer()

        async with ShazamQuery(url) as qry:
            await qry.process()

        if not qry.success:
            raise QueryFailed(
                f"No music found for this media..", query="", full_query=url
            )

        e: Embed = embed.music_found_message(inter.author, qry.info)
        await inter.edit_original_message(embed=e)

    @commands.slash_command()
    @commands.cooldown(1, 10.0, BucketType.guild)
    @commands.max_concurrency(1, BucketType.guild)
    async def share(self, inter: CommandInteraction, url: str):
        """
        Share the song at the given url. It return all the available streaming platform for the track.
        Parameters
        ----------
        inter: The inter
        url: The url of the music/album to share

        Returns
        -------

        """
        if not regex.is_url(url):
            raise commands.UserInputError("You must provide an URL.")

        await inter.response.defer()

        base_url = "https://api.song.link/v1-alpha.1/links?url=%s"
        code, data = await aioweb.cached_query(base_url % parse.quote(url))

        if code != 200:
            raise commands.UserInputError("The URL didn't return anything")

        content = " | ".join(
            f"[{k.capitalize()}]({v['url']})"
            for k, v in sorted(data["linksByPlatform"].items(), key=lambda x: x)
        )
        title: str = data["entitiesByUniqueId"][data["entityUniqueId"]].get(
            "title", "Unknown title"
        )
        artist: str = data["entitiesByUniqueId"][data["entityUniqueId"]].get(
            "artistName", "Unknown artist"
        )
        img: str = data["entitiesByUniqueId"][data["entityUniqueId"]].get(
            "thumbnailUrl", ""
        )
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
