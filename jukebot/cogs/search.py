import os

import nextcord.ui
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import Context, Bot, BucketType

from jukebot.checks import VoiceChecks
from jukebot.components import Query, ResultSet
from jukebot.utils import embed


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def _search_process(self, ctx: Context, query: str, source: str):
        with ctx.typing():
            qry: Query = Query(f"{source}{query}")
            await qry.search()
            if not qry.success:
                e = embed.music_not_found_message(
                    ctx,
                    title=f"Nothing found for {query}, sorry..",
                )
                msg = await ctx.send(embed=e)
                await msg.delete(delay=5.0)
                return

            results: ResultSet = ResultSet.from_query(qry)
            e = embed.search_result_message(
                ctx,
                playlist=results,
                title=f"Result for {query}",
            )

        v = SearchDropdownView(ctx, results)
        msg = await ctx.send(embed=e, view=v)
        await v.wait()
        await msg.edit(view=None)
        result: str = v.result
        if result == SearchInteraction.CANCEL_TEXT:
            e = embed.music_search_message(
                ctx,
                title=f"Search canceled",
            )
            await msg.edit(embed=e)
            await msg.delete(delay=5.0)
            return
        await self.bot.get_cog("Music").play(context=ctx, query=result)
        await msg.delete()

    @commands.command(
        aliases=["sc", "ssc"],
        brief="Search a song on SoundCloud",
        help="Search a query on SoundCloud and display the 10 first results",
        usage="<query>",
        hidden=True,
    )
    @commands.max_concurrency(1, BucketType.user)
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(VoiceChecks.user_is_connected)
    async def soundcloud(self, ctx: Context, *, query: str):
        raise NotImplementedError
        # issue with yt_dlp, scsearch never stop, even if we put the option 'playlistend'
        # await self._search_process(ctx, query, "scsearch10:")

    @commands.command(
        aliases=["yt", "syt"],
        brief="Search a song on YouTube",
        help="Search a query on YouTube and display the 10 first results",
        usage="<query>",
    )
    @commands.max_concurrency(1, BucketType.user)
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(VoiceChecks.user_is_connected)
    async def youtube(self, ctx: Context, *, query: str):
        await self._search_process(ctx, query, "ytsearch10:")


def setup(bot):
    bot.add_cog(Search(bot))


class SearchCanceledException(Exception):
    pass


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
    def __init__(self, ctx: Context, results: ResultSet):
        super().__init__(timeout=float(os.environ["BOT_SEARCH_TIMEOUT"]))
        self._ctx = ctx
        self._drop = SearchDropdown(results)
        self.add_item(self._drop)
        self._timeout = False

    async def interaction_check(self, interaction: Interaction):
        if self._ctx.author != interaction.user:
            return

        self.stop()

    async def on_timeout(self) -> None:
        self._timeout = True

    @property
    def result(self):
        return (
            self._drop.values[0] if not self._timeout else SearchInteraction.CANCEL_TEXT
        )
