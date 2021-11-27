from nextcord import Embed
from nextcord.ext import commands
from nextcord.ext.commands import Context, BucketType, Bot

from jukebot.checks import VoiceChecks
from jukebot.components import AudioStream, Player, PlayerCollection, Song, Query
from jukebot.utils import embed


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self._players: PlayerCollection = PlayerCollection(bot)

    @commands.command(
        aliases=["p"],
        brief="Play a music from url or query",
        help="Play a music from the provided URL or a query",
        usage="<url|query_str>",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(VoiceChecks.user_is_connected)
    async def play(self, ctx: Context, *, query: str):
        with ctx.typing():
            qry: Query = Query(query)
            await qry.process()
            if not qry.success:
                e = embed.music_not_found_message(
                    ctx,
                    title=f"Nothing found for {query}, sorry..",
                )
                await ctx.send(embed=e)
                return

        song: Song = Song.from_query(qry)
        e: Embed = embed.music_message(ctx, song)

        # PlayerContainer create bot if needed
        player: Player = self._players[ctx.guild.id]
        if not player.connected:
            await ctx.invoke(self.join)
        await player.play(ctx, song)
        await ctx.send(embed=e)

    @commands.command(
        aliases=["l"],
        brief="Disconnect the bot from a voice channel",
        help="Disconnect the bot from the current connected voice channel.",
    )
    @commands.guild_only()
    @commands.check(VoiceChecks.bot_is_connected)
    @commands.check(VoiceChecks.bot_and_user_in_same_channel)
    async def leave(self, ctx: Context):
        e = embed.basic_message(ctx, title="Player disconnected")
        await ctx.send(embed=e)
        await self._players[ctx.guild.id].disconnect()
        # once the bot leave, we destroy is ref from the container
        del self._players[ctx.guild.id]

    @commands.command(
        brief="Stop the current music",
        help="Stop the current music from the bot without disconnect him.",
    )
    @commands.guild_only()
    @commands.check(VoiceChecks.bot_is_connected)
    @commands.check(VoiceChecks.bot_and_user_in_same_channel)
    async def stop(self, ctx: Context):
        self._players[ctx.guild.id].stop()
        e = embed.basic_message(ctx, title="Player stopped")
        await ctx.send(embed=e)

    @commands.command(
        brief="Pause the current music",
        help="Pause the current music from the bot without stop it.",
    )
    @commands.guild_only()
    @commands.check(VoiceChecks.bot_is_connected)
    @commands.check(VoiceChecks.bot_and_user_in_same_channel)
    async def pause(self, ctx: Context):
        self._players[ctx.guild.id].pause()
        e = embed.basic_message(ctx, title="Player paused")
        await ctx.send(embed=e)

    @commands.command(
        brief="Resume the current music",
        help="Resume the current music from the bot.",
    )
    @commands.guild_only()
    @commands.check(VoiceChecks.bot_is_connected)
    @commands.check(VoiceChecks.bot_and_user_in_same_channel)
    async def resume(self, ctx: Context):
        self._players[ctx.guild.id].resume()
        e = embed.basic_message(ctx, title="Player resumed")
        await ctx.send(embed=e)

    @commands.command(
        aliases=["np", "now", "now_playing", "curr", "c"],
        brief="Display the current music",
        help="Display the current music and the progression from the bot.",
    )
    @commands.guild_only()
    @commands.check(VoiceChecks.bot_is_connected)
    @commands.check(VoiceChecks.bot_and_user_in_same_channel)
    async def current(self, ctx: Context):
        player: Player = self._players[ctx.guild.id]
        stream: AudioStream = player.stream
        song: Song = player.song
        e = embed.music_message(ctx, song=song, current_duration=stream.progress)
        await ctx.send(embed=e)

    @commands.command(
        aliases=["j", "summon", "invoke"],
        brief="Connect the bot to your current voice channel",
        help="Connect the bot to your current voice channel without playing anything",
    )
    @commands.guild_only()
    @commands.check(VoiceChecks.user_is_connected)
    @commands.check(VoiceChecks.bot_is_not_connected)
    async def join(self, ctx: Context):
        player: Player = self._players[ctx.guild.id]
        await player.join(ctx.message.author.voice.channel)
        e = embed.basic_message(
            ctx, title=f"Connected to {ctx.message.author.voice.channel.name}"
        )
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Music(bot))
