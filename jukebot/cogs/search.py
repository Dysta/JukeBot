from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType
from loguru import logger

from jukebot import components
from jukebot.checks import voice
from jukebot.exceptions import QueryCanceled, QueryFailed
from jukebot.services.music import PlayService
from jukebot.utils import embed
from jukebot.views import SearchDropdownView, SearchInteraction

if TYPE_CHECKING:
    from jukebot.components import Query, ResultSet, SongSet


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.max_concurrency(1, BucketType.user)
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.user_is_connected)
    async def search(
        self,
        inter: CommandInteraction,
        query: str,
        source: commands.option_enum(
            {"YouTube": "ytsearch10:", "SoundCloud": "scsearch10:"}
        ) = "ytsearch10:",
    ):
        """
        Search for your query and display the 10 first results
        Parameters
        ----------
        inter: The interaction
        query: The query to search
        source: The website to use to search for the query

        Returns
        -------

        """
        await inter.response.defer()
        logger.opt(lazy=True).debug(
            f"Search query '{source}{query}' for guild '{inter.guild.name} (ID: {inter.guild.id})'."
        )

        qry: Query = components.Query(f"{source}{query}")
        if "sc" in source:
            await qry.process()
        else:
            await qry.search()
        if not qry.success:
            raise QueryFailed(
                f"Nothing found for {query}",
                query=query,
                full_query=f"{source}{query}",
            )

        results: ResultSet = (
            components.ResultSet.from_query(qry)
            if not "sc" in source
            else SongSet.from_query(qry)
        )
        logger.opt(lazy=True).debug(f"Results of the query is {results}")

        if not results:
            raise QueryFailed(
                f"Nothing found for {query}", query=query, full_query=f"{source}{query}"
            )

        e = embed.search_result_message(
            inter.author,
            playlist=results,
            title=f"Result for {query}",
        )

        v = SearchDropdownView(inter.author, results)
        await inter.edit_original_message(embed=e, view=v)
        await v.wait()
        await inter.edit_original_message(view=None)
        result: str = v.result
        if result == SearchInteraction.CANCEL_TEXT:
            raise QueryCanceled(
                "Search Canceled", query=query, full_query=f"{source}{query}"
            )

        logger.opt(lazy=True).debug(
            f"Query '{source}{query}' successful for guild '{inter.guild.name} (ID: {inter.guild.id})'."
        )

        with PlayService(self.bot) as ps:
            func = ps(interaction=inter, query=result)
        asyncio.ensure_future(func, loop=self.bot.loop)


def setup(bot):
    bot.add_cog(Search(bot))
