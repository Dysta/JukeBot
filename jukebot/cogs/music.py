import utils

from embed import Embed
from discord.ext import commands
from music_components import Player, Request, PlayerCollection


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._players: PlayerCollection = PlayerCollection(bot)

    @commands.command(
        aliases=["p"],
        brief="Play a music from url or query",
        help="Play a music from the provided URL or a query",
        usage="play [url|query_str]",
    )
    @commands.guild_only()
    async def play(self, ctx, *, query: str):
        msg = await ctx.send(f"🔎 searching for `{query}`..")
        req: Request = Request(query)
        await req.process()
        if not req.success:
            await msg.edit(content=f"❌ No match, sorry {ctx.author.mention}")
            return

        e = Embed.music_message(ctx, title=req.title, url=req.web_url)
        e.add_field(name="Channel", value=req.channel)
        duration_str = ""
        if req.live:
            duration_str = "∞"
        else:
            time = utils.seconds_converter(req.duration)
            duration_str = utils.convert_time_to_youtube_format(time)

        e.add_field(name="Duration", value=duration_str)
        if req.thumbnail:
            e.set_image(url=req.thumbnail)

        # PlayerContainer create bot if needed
        player: Player = self._players[ctx.guild.id]
        await player.play(ctx, req)
        await msg.edit(content="⬇ **Found this** ⬇", embed=e)

    @commands.command(
        aliases=["l"],
        brief="Disconnect the bot from a voice channel",
        help="Disconnect the bot from the current connected voice channel.",
        usage="leave",
    )
    @commands.guild_only()
    async def leave(self, ctx):
        if ctx.guild.id in self._players:
            await ctx.send("Ok bye 👋")
            await self._players[ctx.guild.id].disconnect()
            # once the bot leave, we destroy is ref from the container
            del self._players[ctx.guild.id]
        else:
            raise Exception("Player not in container")

    @commands.command(
        brief="Stop the current music",
        help="Stop the current music from the bot without disconnect him.",
        usage="stop",
    )
    @commands.guild_only()
    async def stop(self, ctx):
        if ctx.guild.id in self._players:
            await ctx.send("Ok 🔇")
            self._players[ctx.guild.id].stop()
        else:
            raise Exception("Player not in container")

    @commands.command(
        brief="pause the current music",
        help="pause the current music from the bot without disconnect him.",
        usage="pause",
    )
    @commands.guild_only()
    async def pause(self, ctx):
        if ctx.guild.id in self._players:
            await ctx.send("Ok ⏸")
            self._players[ctx.guild.id].pause()
        else:
            raise Exception("Player not in container")

    @commands.command(
        brief="pause the current music",
        help="pause the current music from the bot without disconnect him.",
        usage="pause",
    )
    @commands.guild_only()
    async def resume(self, ctx):
        if ctx.guild.id in self._players:
            await ctx.send("Ok ▶")
            self._players[ctx.guild.id].resume()
        else:
            raise Exception("Player not in container")


def setup(bot):
    bot.add_cog(Music(bot))
