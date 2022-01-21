from loguru import logger

from nextcord.ext import commands
from nextcord.ext.commands import Bot, Context, BucketType

from jukebot.checks import voice
from jukebot.cogs.search import Search
from jukebot.components import ResultSet, Result


class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def _radio_process(self, ctx: Context, query: str):
        results: ResultSet = await Search._search(ctx, query, "ytsearch10:")
        logger.opt(lazy=True).debug(f"Results are {results}")
        if not results:
            return

        rst: Result = results.get_random_result()
        logger.opt(lazy=True).debug(f"Chosen result is '{rst.title}'")
        music_cog = self.bot.get_cog("Music")
        await ctx.invoke(music_cog.play, query=rst.web_url)

    @commands.group(
        aliases=["rd"],
        brief="Launch a radio",
        help="Launch a radio",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def radio(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.list)

    @radio.command(
        aliases=["all"],
        brief="Return all available radio.",
        help="Return all available radio.",
    )
    async def list(self, ctx: Context):
        subcmds = ", ".join(
            [c.name for c in sorted(self.radio.commands, key=lambda c: c.name)]
        )
        await ctx.reply(
            content=f"Use `{ctx.clean_prefix}radio <radio_name>` to launch a radio. Available radio name:\n{subcmds}",
            mention_author=False,
        )

    @radio.command()
    @commands.check(voice.user_is_connected)
    async def lofi(self, ctx: Context):
        await self._radio_process(ctx, "lofi")

    @radio.command()
    @commands.check(voice.user_is_connected)
    async def jazz(self, ctx: Context):
        await self._radio_process(ctx, "jazz live")

    @radio.command(aliases=["rnr", "r&r"])
    @commands.check(voice.user_is_connected)
    async def rocknroll(self, ctx: Context):
        await self._radio_process(ctx, "rock n roll radio")

    @radio.command(aliases=["ct", "8bits"])
    @commands.check(voice.user_is_connected)
    async def chiptune(self, ctx: Context):
        await self._radio_process(ctx, "chiptune radio")

    @radio.command(aliases=["sw", "vw", "vaporwave"])
    @commands.check(voice.user_is_connected)
    async def synthwave(self, ctx: Context):
        await self._radio_process(ctx, "synthwave radio")

    @radio.command(aliases=["coffee", "loungecoffee"])
    @commands.check(voice.user_is_connected)
    async def lounge(self, ctx: Context):
        await self._radio_process(ctx, "lounge coffee radio")

    @radio.command(aliases=["mc"])
    @commands.check(voice.user_is_connected)
    async def minecraft(self, ctx: Context):
        await self._radio_process(ctx, "minecraft radio")

    @radio.command()
    @commands.check(voice.user_is_connected)
    async def rap(self, ctx: Context):
        await self._radio_process(ctx, "rap radio")


def setup(bot):
    bot.add_cog(Radio(bot))
