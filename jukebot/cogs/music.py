from discord.ext import commands
from discord.ext.commands import Context

from jukebot.components import Player, Request, PlayerCollection
from jukebot.utils import embed
from jukebot.components import Song


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._players: PlayerCollection = PlayerCollection(bot)

    @commands.command(
        aliases=["p"],
        brief="Play a music from url or query",
        help="Play a music from the provided URL or a query",
        usage="<url|query_str>",
    )
    @commands.guild_only()
    async def play(self, ctx: Context, *, query: str):
        e = embed.music_search_message(ctx, title=f"Searching for {query}..")
        msg = await ctx.send(embed=e)
        req: Request = Request(query)
        await req.process()
        if not req.success:
            e = embed.music_not_found_message(
                ctx,
                title=f"Nothing found for {query}, sorry..",
            )
            await msg.edit(embed=e)
            return

        song: Song = Song.from_request(req)
        e = embed.music_message(ctx, song)

        # PlayerContainer create bot if needed
        player: Player = self._players[ctx.guild.id]
        await player.play(ctx, song)
        await msg.edit(embed=e)

    @commands.command(
        aliases=["l"],
        brief="Disconnect the bot from a voice channel",
        help="Disconnect the bot from the current connected voice channel.",
    )
    @commands.guild_only()
    async def leave(self, ctx: Context):
        if ctx.guild.id in self._players:
            e = embed.basic_message(ctx, title="Player disconnected")
            await ctx.send(embed=e)
            await self._players[ctx.guild.id].disconnect()
            # once the bot leave, we destroy is ref from the container
            del self._players[ctx.guild.id]
        else:
            raise Exception("Player not in container")

    @commands.command(
        brief="Stop the current music",
        help="Stop the current music from the bot without disconnect him.",
    )
    @commands.guild_only()
    async def stop(self, ctx: Context):
        if ctx.guild.id in self._players:
            e = embed.basic_message(ctx, title="Player stopped")
            await ctx.send(embed=e)
            self._players[ctx.guild.id].stop()
        else:
            raise Exception("Player not in container")

    @commands.command(
        brief="Pause the current music",
        help="Pause the current music from the bot without stop it.",
    )
    @commands.guild_only()
    async def pause(self, ctx: Context):
        if ctx.guild.id in self._players:
            e = embed.basic_message(ctx, title="Player paused")
            await ctx.send(embed=e)
            self._players[ctx.guild.id].pause()
        else:
            raise Exception("Player not in container")

    @commands.command(
        brief="Resume the current music",
        help="Resume the current music from the bot.",
    )
    @commands.guild_only()
    async def resume(self, ctx: Context):
        if ctx.guild.id in self._players:
            e = embed.basic_message(ctx, title="Player resumed")
            await ctx.send(embed=e)
            self._players[ctx.guild.id].resume()
        else:
            raise Exception("Player not in container")


def setup(bot):
    bot.add_cog(Music(bot))
