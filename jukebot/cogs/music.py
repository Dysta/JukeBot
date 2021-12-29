from datetime import datetime
from typing import Optional

from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import Context, BucketType, Bot

from jukebot.checks import voice
from jukebot.components import (
    AudioStream,
    Player,
    Song,
    Query,
    Result,
    ResultSet,
)
from jukebot.utils import embed, regex, converter


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.command(
        aliases=["p"],
        brief="Play a music from url or query",
        help="Play a music from the provided URL or a query",
        usage="<url|query_str>",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.user_is_connected)
    async def play(
        self,
        ctx: Context,
        author: Optional[Member] = None,
        force: Optional[bool] = False,
        *,
        query: str,
    ):
        # PlayerContainer create bot if needed
        player: Player = self.bot.players[ctx.guild.id]
        author = author or ctx.author
        if not player.context:
            await ctx.invoke(self.bind)

        if not force and player.playing:
            await ctx.invoke(self.add, query=query)
            return

        with ctx.typing():
            qry: Query = Query(query)
            await qry.process()
            if not qry.success:
                e = embed.music_not_found_message(
                    author,
                    title=f"Nothing found for {query}, sorry..",
                )
                await ctx.send(embed=e)
                return

        song: Song = Song.from_query(qry)
        song.requester = author

        if not player.connected:
            await ctx.invoke(self.join)
        await player.play(song)
        e: Embed = embed.music_message(author, song)
        await ctx.send(embed=e)

    @commands.command(
        aliases=["l"],
        brief="Disconnect the bot from a voice channel",
        help="Disconnect the bot from the current connected voice channel.",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def leave(self, ctx: Context):
        await self.bot.players[ctx.guild.id].disconnect()
        # once the bot leave, we destroy is instance from the container
        del self.bot.players[ctx.guild.id]
        e = embed.basic_message(ctx.author, title="Player disconnected")
        await ctx.send(embed=e)

    @commands.command(
        brief="Stop the current music",
        help="Stop the current music from the bot without disconnect him.",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def stop(self, ctx: Context, silent: Optional[bool] = False):
        self.bot.players[ctx.guild.id].stop()
        if not silent:
            e = embed.basic_message(ctx.author, title="Player stopped")
            await ctx.send(embed=e)

    @commands.command(
        brief="Pause the current music",
        help="Pause the current music from the bot without stop it.",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def pause(self, ctx: Context):
        self.bot.players[ctx.guild.id].pause()
        e = embed.basic_message(ctx.author, title="Player paused")
        await ctx.send(embed=e)

    @commands.command(
        brief="Resume the current music",
        help="Resume the current music from the bot.",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def resume(self, ctx: Context):
        self.bot.players[ctx.guild.id].resume()
        e = embed.basic_message(ctx.author, title="Player resumed")
        await ctx.send(embed=e)

    @commands.command(
        aliases=["np", "now", "now_playing", "curr", "c"],
        brief="Display the current music",
        help="Display the current music and the progression from the bot.",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def current(self, ctx: Context):
        player: Player = self.bot.players[ctx.guild.id]
        stream: AudioStream = player.stream
        song: Song = player.song
        if stream and song:
            e = embed.music_message(
                song.requester, song=song, current_duration=stream.progress
            )
        else:
            e = embed.basic_message(
                ctx.author,
                title="Nothing is currently playing",
                content=f"Try `{ctx.prefix}play` to add a music !",
            )
        await ctx.send(embed=e)

    @commands.command(
        aliases=["j", "summon", "invoke"],
        brief="Connect the bot to your current voice channel",
        help="Connect the bot to your current voice channel without playing anything",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.user_is_connected)
    @commands.check(voice.bot_is_not_connected)
    async def join(self, ctx: Context):
        player: Player = self.bot.players[ctx.guild.id]
        await player.join(ctx.message.author.voice.channel)
        e = embed.basic_message(
            ctx.author,
            title=f"Player connected to {ctx.message.author.voice.channel.name}",
        )
        await ctx.send(embed=e)

    @commands.command(
        aliases=["a"],
        brief="Add a song to the current queue",
        help="Add a song to the current player queue",
        usage="<url|query_str>",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def add(self, ctx: Context, *, query: str):
        query = query if regex.is_url(query) else f"ytsearch1:{query}"
        with ctx.typing():
            qry: Query = Query(query)
            await qry.search()
            if not qry.success:
                e = embed.music_not_found_message(
                    ctx.author,
                    title=f"Nothing found for {query}, sorry..",
                )
                await ctx.send(embed=e)
                return

        res: Result = Result.from_query(qry)
        res.requester = ctx.author
        player: Player = self.bot.players[ctx.guild.id]
        player.queue.put(res)

        e: Embed = embed.result_enqueued(ctx.author, res)
        await ctx.send(embed=e)

    @commands.command(
        aliases=["q", "list"],
        brief="Show the queue of the server.",
        help="Show the queue of the server",
    )
    @commands.guild_only()
    @commands.cooldown(1, 3.0, BucketType.user)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def queue(self, ctx: Context):
        queue: ResultSet = self.bot.players[ctx.guild.id].queue
        e: Embed = embed.queue_message(
            ctx.author, queue, title=f"Queue for {ctx.guild.name}"
        )
        await ctx.send(embed=e)

    @commands.command(
        aliases=["s", "next"],
        brief="Skip the current song.",
        help="Skip the current song and play the next one.",
    )
    @commands.guild_only()
    @commands.cooldown(3, 10.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def skip(self, ctx: Context):
        queue: ResultSet = self.bot.players[ctx.guild.id].queue
        keep_playing: bool = len(queue) > 0
        if keep_playing:
            e: embed = embed.basic_message(ctx.author, title="Skipped !")
            await ctx.send(embed=e)
        await ctx.invoke(self.stop, silent=keep_playing)

    @commands.command(
        aliases=["b", "link"],
        brief="Bind a voice channel to the bot.",
        help="Bind the current text channel to the bot. The channel will be used to send information about the bot status.",
    )
    @commands.guild_only()
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.guild)
    async def bind(self, ctx: Context):
        e: embed = embed.basic_message(
            ctx.author, title=f"Binded to {ctx.channel.name}"
        )
        msg = await ctx.send(embed=e)
        # we put the bot message as a context to avoid displaying
        # the user who invoke the command to appear in system message
        player: Player = self.bot.players[ctx.guild.id]
        ctx = await self.bot.get_context(msg)
        player.context = ctx

    @commands.command(
        aliases=["time"],
        brief="Set the current song to a defined time.",
        help="Set the song to the given timecode.\n"
        "HH, for hour, is a integer between 0 and 24.\n"
        "MM, for minute, is an integer between 0 and 59.\n"
        "SS, for second, is a integer between 0 and 59.",
        usage="<[[HH:]MM:]:SS>",
    )
    @commands.guild_only()
    @commands.check(voice.bot_not_playing_live)
    @commands.check(voice.bot_is_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.guild)
    async def seek(self, ctx: Context, time_string: str):
        count = time_string.count(":")
        if count == 2:
            fmt = "%H:%M:%S"
        elif count == 1:
            fmt = "%M:%S"
        else:
            fmt = "%S"

        try:
            fmt_date = datetime.strptime(time_string, fmt)
        except:
            raise commands.UserInputError(
                f"Incorrect timecode `{time_string}`, see **{ctx.prefix}help seek**."
            )

        sec = int((fmt_date - datetime(1900, 1, 1)).total_seconds())
        await self.bot.players[ctx.guild.id].seek(sec)

        fmt_sec = converter.seconds_to_youtube_format(sec)
        e = embed.basic_message(ctx.author, content=f"Time set to `{fmt_sec}`.")
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Music(bot))
