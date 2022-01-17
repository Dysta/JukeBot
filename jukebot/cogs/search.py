import asyncio
import os

import nextcord.ui

from loguru import logger

from nextcord import Interaction, Member
from nextcord.ext import commands
from nextcord.ext.commands import Context, Bot, BucketType

from jukebot.checks import voice
from jukebot.components import Query, ResultSet, SongSet
from jukebot.utils import embed


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def _search_process(self, ctx: Context, query: str, source: str):
        logger.opt(lazy=True).debug(
            f"Search query '{source}{query}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
        )
        with ctx.typing():
            qry: Query = Query(f"{source}{query}")
            if "sc" in source:
                await qry.process()
            else:
                await qry.search()
            if not qry.success:
                logger.opt(lazy=True).debug(
                    f"Query '{source}{query}' failed for guild '{ctx.guild.name} (ID: {ctx.guild.id})'.."
                )
                e = embed.music_not_found_message(
                    ctx.author,
                    title=f"Nothing found for {query}, sorry..",
                )
                msg = await ctx.send(embed=e)
                await msg.delete(delay=5.0)
                return

            results: ResultSet = (
                ResultSet.from_query(qry)
                if not "sc" in source
                else SongSet.from_query(qry)
            )
            logger.opt(lazy=True).debug(f"Results of the query is {results}")

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
            logger.opt(lazy=True).debug(
                f"Query '{source}{query}' canceled for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
            )
            e = embed.music_not_found_message(
                ctx.author,
                title=f"Search canceled",
            )
            await msg.edit(embed=e, delete_after=5.0)
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


class SearchInteraction:
    CANCEL_REACTION = "❌"
    CANCEL_TEXT = "Cancel"
    NUMBER_REACTION = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
        "🔟",
    ]


class SearchDropdown(nextcord.ui.Select):
    def __init__(self, results: ResultSet):
        self._results = results
        options = [
            nextcord.SelectOption(
                label=r.title,
                value=r.web_url,
                description=f"on {r.channel} — {r.fmt_duration}",
                emoji=SearchInteraction.NUMBER_REACTION[i],
            )
            for i, r in enumerate(results)
        ]
        options.append(
            nextcord.SelectOption(
                label="Cancel",
                value=SearchInteraction.CANCEL_TEXT,
                description="Cancel the current search",
                emoji=SearchInteraction.CANCEL_REACTION,
            )
        )

        super().__init__(
            placeholder="Choose a song...",
            min_values=1,
            max_values=1,
            options=options,
        )


class SearchDropdownView(nextcord.ui.View):
    def __init__(self, author: Member, results: ResultSet):
        super().__init__(timeout=float(os.environ["BOT_SEARCH_TIMEOUT"]))
        self._author = author
        self._drop = SearchDropdown(results)
        self.add_item(self._drop)
        self._timeout = False

    async def interaction_check(self, interaction: Interaction):
        if self._author != interaction.user:
            return
        self.stop()

    async def on_timeout(self) -> None:
        self._timeout = True

    @property
    def result(self):
        return (
            self._drop.values[0] if not self._timeout else SearchInteraction.CANCEL_TEXT
        )
