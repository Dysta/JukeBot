from typing import Optional

from nextcord import Embed
from nextcord.ext import commands
from nextcord.ext.commands import Context, BucketType, Bot

from jukebot.checks import voice, user
from jukebot.components import (
    AudioStream,
    Player,
    Song,
    Query,
    Result,
    ResultSet,
)
from jukebot.utils import embed, regex


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
    async def play(self, ctx: Context, *, query: str):
        # PlayerContainer create bot if needed
        player: Player = self.bot.players[ctx.guild.id]
        if not player.context:
            await ctx.invoke(self.bind)

        if query:
            await ctx.invoke(self.add, silent=bool(not player.playing), query=query)
        if player.playing:
            return

        with ctx.typing():
            rqs: Result = player.queue.get()
            author = rqs.requester
            qry: Query = Query(rqs.web_url)
            await qry.process()
            if not qry.success:
                e = embed.music_not_found_message(
                    author,
                    title=f"Nothing found for {rqs.title}, sorry..",
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
    @commands.check(voice.bot_is_playing)
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
    async def add(self, ctx: Context, silent: Optional[bool] = False, *, query: str):
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

        if qry.type == Query.Type.PLAYLIST:
            res: ResultSet = ResultSet.from_query(qry, ctx.author)
            player: Player = self.bot.players[ctx.guild.id]
            player.queue += res

            e: Embed = embed.queue_message(
                ctx.author, res, title=f"Enqueued : {len(res)} songs"
            )
            await ctx.send(embed=e)
        else:
            res: Result = Result.from_query(qry)
            res.requester = ctx.author
            player: Player = self.bot.players[ctx.guild.id]
            player.queue.put(res)
            if not silent:
                e: Embed = embed.result_enqueued(ctx.author, res)
                await ctx.send(embed=e)

    @commands.command(
        aliases=["r"],
        brief="Remove a song from the current queue.",
        help="Remove the song at pos `idx` of the queue",
        usage="<idx>",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(user.bot_queue_is_not_empty)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def remove(self, ctx: Context, idx: int):
        queue: ResultSet = self.bot.players[ctx.guild.id].queue
        if not (elem := queue.remove(idx - 1)):
            raise commands.UserInputError(f"Can't delete item number {idx}")

        e: Embed = embed.basic_message(
            ctx.author, content=f"`{elem.title}` have been removed from the queue"
        )
        await ctx.send(embed=e)

    @commands.command(
        aliases=["clr"],
        brief="Clear the current queue.",
        help="Remove all the songs of the queue",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(user.bot_queue_is_not_empty)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def clear(self, ctx: Context):
        player: Player = self.bot.players[ctx.guild.id]
        player.queue = ResultSet.empty()

        e: Embed = embed.basic_message(ctx.author, title="The queue have been cleared.")
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
    @commands.check(voice.bot_is_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def skip(self, ctx: Context):
        queue: ResultSet = self.bot.players[ctx.guild.id].queue
        keep_playing: bool = not queue.is_empty()
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


def setup(bot):
    bot.add_cog(Music(bot))
