from __future__ import annotations

from typing import Optional
from urllib import parse

from disnake import APISlashCommand, CommandInteraction, Embed, Forbidden
from disnake.ext import commands
from disnake.ext.commands import BucketType

from jukebot import JukeBot
from jukebot.components.player import Player
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
        self.bot: JukeBot = bot

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
        if self.bot.players.get(inter.guild.id).is_playing:
            # ? if player is playing, play command is just a shortcut for queue add command
            await self.bot.get_slash_command("queue add").callback(self, inter, query, top)
            return

        if not inter.response.is_done():
            await inter.response.defer()

        song, loop = await self.bot.services.play(interaction=inter, query=query, top=top)

        e: Embed = embed.music_message(song, loop)
        await inter.edit_original_message(embed=e)

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
        await self.bot.services.leave(guild_id=inter.guild.id)

        e = embed.basic_message(title="Player disconnected")
        await inter.send(embed=e)

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
        await self.bot.services.stop(guild_id=inter.guild.id)

        e = embed.basic_message(title="Player stopped")
        await inter.send(embed=e)

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
        await self.bot.services.pause(guild_id=inter.guild.id)

        e = embed.basic_message(title="Player paused")
        await inter.send(embed=e)

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
        player: Player = self.bot.players[inter.guild.id]
        if player.state.is_stopped and not player.queue.is_empty():
            # ? if player is stopped but queue isn't empty, resume the queue
            await self.bot.get_slash_command("play").callback(self, inter, query="")
            return

        ok = await self.bot.services.resume(guild_id=inter.guild.id)

        if ok:
            e = embed.basic_message(title="Player resumed")
        else:
            cmd: APISlashCommand = self.bot.get_global_command_named("play")
            e = embed.basic_message(
                title="Nothing is currently playing", content=f"Try </play:{cmd.id}> to add a music !"
            )

        await inter.send(embed=e)

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
        song, stream, loop = await self.bot.services.current_song(guild_id=inter.guild.id)

        if stream and song:
            e = embed.music_message(song, loop, stream.progress)
        else:
            cmd: APISlashCommand = self.bot.get_global_command_named("play")
            e = embed.basic_message(
                title="Nothing is currently playing", content=f"Try </play:{cmd.id}> to add a music !"
            )

        await inter.send(embed=e)

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
        await self.bot.services.join(interaction=inter)

        e = embed.basic_message(
            content=f"Connected to <#{inter.author.voice.channel.id}>\n" f"Bound to <#{inter.channel.id}>\n",
        )
        await inter.send(embed=e)

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
        await self.bot.services.skip(guild_id=inter.guild.id)

        e: embed = embed.basic_message(title="Skipped !")
        await inter.send(embed=e)

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
        song, stream = await self.bot.services.grab(guild_id=inter.guild.id)

        e = embed.grab_message(song, stream.progress)
        e.add_field(
            name="Voice channel",
            value=f"`{inter.guild.name} — {inter.author.voice.channel.name}`",
        )
        try:
            await inter.author.send(embed=e)
            await inter.send("Check your DMs!", ephemeral=True)
        except Forbidden:
            await inter.send("Your DMs are closed!", embed=e, ephemeral=True)

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
        new_status = await self.bot.services.loop(guild_id=inter.guild.id, mode=mode)

        e: embed = embed.basic_message(title=new_status)
        await inter.send(embed=e)

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


def setup(bot: JukeBot):
    bot.add_cog(Music(bot))

    bot.add_service(GrabService(bot))
    bot.add_service(JoinService(bot))
    bot.add_service(LeaveService(bot))
    bot.add_service(LoopService(bot))
    bot.add_service(PauseService(bot))
    bot.add_service(PlayService(bot))
    bot.add_service(ResumeService(bot))
    bot.add_service(SkipService(bot))
    bot.add_service(StopService(bot))
    bot.add_service(CurrentSongService(bot))
