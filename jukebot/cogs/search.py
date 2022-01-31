import asyncio
from typing import Optional

from loguru import logger

from nextcord.ext import commands
from nextcord.ext.commands import Context, Bot, BucketType

from jukebot.checks import voice
from jukebot.components import Query, ResultSet, SongSet
from jukebot.utils import embed, query_callback
from jukebot.views import SearchDropdownView, SearchInteraction


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @staticmethod
    async def _search(ctx: Context, query: str, source: str) -> Optional[ResultSet]:
        logger.opt(lazy=True).debug(
            f"Search query '{source}{query}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
        )

        qry: Query = Query(f"{source}{query}")
        if "sc" in source:
            await qry.process()
        else:
            await qry.search()
        if not qry.success:
            return None

        results: ResultSet = (
            ResultSet.from_query(qry) if not "sc" in source else SongSet.from_query(qry)
        )
        logger.opt(lazy=True).debug(f"Results of the query is {results}")
        return results

    async def _search_process(self, ctx: Context, query: str, source: str):
        with ctx.typing():
            results = await Search._search(ctx, query, source)
        if not results:
            await query_callback.failure(ctx, query, f"{source}{query}")
            return

        e = embed.search_result_message(
            ctx.author,
            playlist=results,
            title=f"Result for {query}",
        )

        v = SearchDropdownView(ctx.author, results)
        msg = await ctx.send(embed=e, view=v)
        await v.wait()
        await msg.edit(view=None)
        result: str = v.result
        if result == SearchInteraction.CANCEL_TEXT:
            await query_callback.cancel(ctx, msg, query, f"{source}{query}")
            return

        logger.opt(lazy=True).debug(
            f"Query '{source}{query}' successful for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
        )

        music_cog = self.bot.get_cog("Music")
        func = ctx.invoke(music_cog.play, query=result)
        asyncio.ensure_future(func, loop=self.bot.loop)
        await msg.delete()

    @commands.command(
        aliases=["sc", "ssc"],
        brief="Search a song on SoundCloud",
        help="Search a query on SoundCloud and display the 10 first results",
        usage="<query>",
    )
    @commands.max_concurrency(1, BucketType.user)
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def soundcloud(self, ctx: Context, *, query: str):
        await self._search_process(ctx, query, "scsearch10:")

    @commands.command(
        aliases=["yt", "syt"],
        brief="Search a song on YouTube",
        help="Search a query on YouTube and display the 10 first results",
        usage="<query>",
    )
    @commands.max_concurrency(1, BucketType.user)
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def youtube(self, ctx: Context, *, query: str):
        await self._search_process(ctx, query, "ytsearch10:")


def setup(bot):
    bot.add_cog(Search(bot))
