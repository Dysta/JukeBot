import asyncio
import os

from discord import Reaction, User, Message
from discord.ext import commands
from discord.ext.commands import Context, Bot

from jukebot.components import Player, Query, PlayerCollection, Song, ResultSet
from jukebot.utils import embed, converter


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self._players: PlayerCollection = PlayerCollection(bot)

    async def _search_process(self, ctx: Context, query: str, source: str):
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
            return

        results: ResultSet = ResultSet.from_query(qry)
        e = embed.playlist_message(
            ctx,
            playlist=results,
            title=f"Result for {query}",
        )
        await msg.edit(embed=e)
        await SearchInteraction.add_reaction_to_message(msg, len(results))

        def check(reaction: Reaction, user: User):
            return (
                reaction.emoji in SearchInteraction.ALLOWED_REACTION
                and user == ctx.message.author
            )

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=check,
                timeout=float(os.environ["BOT_SEARCH_TIMEOUT"]),
            )
            await msg.clear_reactions()
            if reaction.emoji == SearchInteraction.CANCEL_REACTION:
                raise SearchCanceledException
            await msg.add_reaction(reaction.emoji)
        except (asyncio.TimeoutError, SearchCanceledException):
            e = embed.music_search_message(ctx, title="Search canceled")
            await msg.clear_reactions()
            await msg.edit(embed=e)
            return

        qry: Query = Query(results[converter.emoji_to_number(reaction.emoji) - 1].url)
        await qry.process()
        song: Song = Song.from_query(qry)
        e = embed.music_message(ctx, song)
        await msg.edit(embed=e)

        # PlayerContainer create bot if needed
        player: Player = self._players[ctx.guild.id]
        await player.play(ctx, song)
        await msg.clear_reactions()

    @commands.command(
        aliases=["sc", "ssc"],
        brief="Search a song on SoundCloud",
        help="Search a query on SoundCloud and display the 10 first results",
        usage="<query>",
        hidden=True,
    )
    @commands.guild_only()
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
    @commands.guild_only()
    async def youtube(self, ctx: Context, *, query: str):
        await self._search_process(ctx, query, "ytsearch10:")


def setup(bot):
    bot.add_cog(Search(bot))


class SearchCanceledException(Exception):
    pass


class SearchInteraction:
    CANCEL_REACTION = "❌"
    ALLOWED_REACTION = [
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
        CANCEL_REACTION,
    ]

    @staticmethod
    async def add_reaction_to_message(msg: Message, end: int = None):
        if not end:
            end = len(SearchInteraction.ALLOWED_REACTION) - 1
        for i in range(1, end + 1):
            await msg.add_reaction(f"{converter.number_to_emoji(i)}")
        await msg.add_reaction(SearchInteraction.CANCEL_REACTION)
