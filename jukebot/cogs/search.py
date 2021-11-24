import os
from typing import Optional

import nextcord.ui
from nextcord import Interaction, Message
from nextcord.ext import commands
from nextcord.ext.commands import Context, Bot, BucketType

from jukebot.checks import VoiceChecks
from jukebot.components import PlayerCollection, Query, ResultSet, Song
from jukebot.utils import embed


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self._players: PlayerCollection = PlayerCollection(bot)

    async def _single_search_process(
        self, ctx: Context, query: str
    ) -> tuple[Message, Optional[Song]]:
        e = embed.music_search_message(ctx, title=f"Searching for {query}..")
        msg = await ctx.send(embed=e)
        qry: Query = Query(query)
        await qry.process()
        if not qry.success:
            e = embed.music_not_found_message(
                ctx,
                title=f"Nothing found for {query}, sorry..",
            )
            await msg.edit(embed=e)
            return msg, None
        song: Song = Song.from_query(qry)
        return msg, song

    async def _search_process(
        self, ctx: Context, query: str, source: str
    ) -> tuple[Message, Optional[ResultSet]]:
        e = embed.music_search_message(ctx, title=f"Searching for {query}..")
        msg = await ctx.send(embed=e)
        qry: Query = Query(f"{source}{query}")
        await qry.search()
        if not qry.success:
            e = embed.music_not_found_message(
                ctx,
                title=f"Nothing found for {query}, sorry..",
            )
            await msg.edit(embed=e)
            return msg, None

        results: ResultSet = ResultSet.from_query(qry)
        return msg, results

    @commands.command(
        aliases=["sc", "ssc"],
        brief="Search a song on SoundCloud",
        help="Search a query on SoundCloud and display the 10 first results",
        usage="<query>",
        hidden=True,
    )
    @commands.max_concurrency(1, BucketType.user)
    @commands.cooldown(1, 3.0, BucketType.user)
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
    @commands.cooldown(1, 3.0, BucketType.user)
    @commands.guild_only()
    @commands.check(VoiceChecks.user_is_connected)
    async def youtube(self, ctx: Context, *, query: str):
        msg, results = await self._search_process(ctx, query, "ytsearch10:")
        e = embed.playlist_message(
            ctx,
            playlist=results,
            title=f"Result for {query}",
        )
        v = SearchDropdownView(ctx, results)
        await msg.edit(embed=e, view=v)
        await v.wait()
        r: str = v.result
        if r == "Cancel":
            e = embed.music_not_found_message(
                ctx,
                title=f"Search canceled",
            )
            await msg.edit(embed=e)
            return
        await msg.delete()
        await self.bot.get_cog("Music").play(context=ctx, query=v.result)


def setup(bot):
    bot.add_cog(Search(bot))


class SearchCanceledException(Exception):
    pass


class SearchInteraction:
    CANCEL_REACTION = "❌"
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
                description=f"on {r.channel} [{r.fmt_duration}]",
                emoji=SearchInteraction.NUMBER_REACTION[i],
            )
            for i, r in enumerate(results)
        ]
        options.append(
            nextcord.SelectOption(
                label="Cancel",
                value="Cancel",
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

    async def interaction_check(self, interaction: Interaction):
        if self._ctx.author != interaction.user:
            return
        await interaction.response.edit_message(
            content=embed.VOID_TOKEN, embed=None, view=None
        )
        self.stop()

    @property
    def result(self):
        return self._drop.values[0]
