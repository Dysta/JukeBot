from datetime import datetime

from loguru import logger
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
)
from jukebot.utils import embed


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
        with ctx.typing():
            if not player.is_connected and not await ctx.invoke(self.join):
                # we delete the player because it means that we have created it for nothing
                self.bot.players.pop(ctx.guild.id)
                return False

        if query:
            queue_cog = self.bot.get_cog("Queue")
            ok: bool = await ctx.invoke(queue_cog.add, query=query)
            if not ok:
                return False

        if player.is_playing:
            return True  # return True bc everything is ok

        with ctx.typing():
            rqs: Result = player.queue.get()
            author = rqs.requester
            qry: Query = Query(rqs.web_url)
            await qry.process()

        song: Song = Song.from_query(qry)
        song.requester = author

        try:
            await player.play(song)
        except Exception as e:
            logger.opt(lazy=True).error(
                f"Server {ctx.guild.name} ({ctx.guild.id}) can't play in its player. Should not happen.\n"
                f"Error: {e}"
            )
            e: Embed = embed.error_message(
                author,
                content="The player cannot play on the voice channel. This is because he's not connected to a voice channel or he's already playing something.\n"
                "This situation can happen when the player has been abruptly disconnected by Discord or a user. "
                "Use the `reset` command to reset the player in this case.",
            )
            await ctx.send(embed=e)
            return False

        e: Embed = embed.music_message(author, song)
        await ctx.send(embed=e)
        return True

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
        # once the bot leave, we destroy is instance from the container
        await self.bot.players.pop(ctx.guild.id).disconnect()
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
    async def stop(self, ctx: Context):
        self.bot.players[ctx.guild.id].stop()
        e = embed.basic_message(ctx.author, title="Player stopped")
        await ctx.send(embed=e)

    @commands.command(
        brief="Pause the current music",
        help="Pause the current music from the bot without stop it.",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_is_playing)
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
    @commands.check(voice.bot_is_not_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def resume(self, ctx: Context):
        player: Player = self.bot.players[ctx.guild.id]
        if player.is_paused:
            player.resume()
            e = embed.basic_message(ctx.author, title="Player resumed")
            await ctx.send(embed=e)
        elif player.state.is_stopped and not player.queue.is_empty():
            await ctx.invoke(self.play, query="")
        else:
            e = embed.basic_message(
                ctx.author,
                title="Nothing to play",
                content=f"Try `{ctx.prefix}play` to add a music !",
            )
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
        try:
            await player.join(ctx.author.voice.channel)
        except:
            logger.opt(lazy=True).error(
                f"Server {ctx.guild.name} ({ctx.guild.id}) can't connect his player to channel {ctx.author.voice.channel.name} ({ctx.author.voice.channel.id})."
            )
            logger.opt(lazy=True).debug(
                f"Channel {ctx.author.voice.channel.name} ({ctx.author.voice.channel.id}) permissions {ctx.author.voice.channel.permissions_for(ctx.me)}."
            )
            e: Embed = embed.error_message(
                ctx.author,
                title=f"Can't connect to {ctx.author.voice.channel.name}",
                content="Check both __bot__ and __channel__ permissions.\n"
                "If the problem persists, use the `reset` command to reset the player. ",
            )
            await ctx.send(embed=e)
            return False

        e = embed.basic_message(
            ctx.author,
            content=f"Connected to <#{ctx.author.voice.channel.id}>\n"
            f"Bound to <#{ctx.channel.id}>\n",
        )
        msg = await ctx.send(embed=e)
        # we put the bot message as a context to avoid displaying
        # the user who invoke the command to appear in system message
        ctx = await self.bot.get_context(msg)
        player.context = ctx
        return True

    @commands.command(
        aliases=["s", "next"],
        brief="Skip the current song.",
        help="Skip the current song and play the next one.",
    )
    @commands.guild_only()
    @commands.cooldown(3, 10.0, BucketType.user)
    @commands.check(voice.bot_is_streaming)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def skip(self, ctx: Context):
        self.bot.players[ctx.guild.id].skip()
        e: embed = embed.basic_message(ctx.author, title="Skipped !")
        await ctx.send(embed=e)

    @commands.command(
        aliases=["dump", "pick", "save"],
        brief="Send the current song in DM to save it.",
        help="Send the current song in DM to save it.",
    )
    @commands.guild_only()
    @commands.check(voice.bot_is_playing)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.user)
    async def grab(self, ctx: Context):
        player: Player = self.bot.players[ctx.guild.id]
        stream: AudioStream = player.stream
        song: Song = player.song
        e = embed.music_message(
            song.requester, song=song, current_duration=stream.progress
        )
        timestamp = int(datetime.now().timestamp())
        await ctx.author.send(
            content=f"Save music from `{ctx.guild.name} — {ctx.author.voice.channel.name}` at <t:{timestamp}:T>",
            embed=e,
        )
        await ctx.message.add_reaction("👍")

    @commands.group(
        aliases=["lp"],
        brief="Loop the current song.",
        help="Allow user to enable or disable the looping of a song.",
    )
    @commands.guild_only()
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    @commands.cooldown(1, 5.0, BucketType.user)
    async def loop(self, ctx: Context):
        if not ctx.invoked_subcommand:
            player: Player = self.bot.players[ctx.guild.id]
            looping: bool = player.loop.is_enabled

            e: embed = embed.basic_message(
                ctx.author, title=f"Loop is {'enabled' if looping else 'disabled'}"
            )
            await ctx.send(embed=e)

    @loop.command(
        name="on",
        aliases=["enable"],
        bried="Enable looping of the current song.",
        help="Repeat the current song when it finish.",
    )
    async def loop_enabled(self, ctx: Context):
        self.bot.players[ctx.guild.id].loop = Player.Loop.ENABLED
        e: embed = embed.basic_message(ctx.author, title="Loop is enabled")
        await ctx.send(embed=e)

    @loop.command(
        name="off",
        aliases=["disable"],
        bried="Disable looping of the current song.",
        help="When a song is finish, pass to the next one instead of repeating itself.",
    )
    async def loop_disabled(self, ctx: Context):
        self.bot.players[ctx.guild.id].loop = Player.Loop.DISABLED
        e: embed = embed.basic_message(ctx.author, title="Loop is disabled")
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Music(bot))
