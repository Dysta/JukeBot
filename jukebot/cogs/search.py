import asyncio
import os

from discord import Reaction, User
from discord.ext import commands
from discord.ext.commands import Context, Bot

from jukebot.components import Player, Request, PlayerCollection, Song
from jukebot.components.playlist import Playlist
from jukebot.utils import embed, converter


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self._players: PlayerCollection = PlayerCollection(bot)

    async def _search_process(self, ctx: Context, query: str, source: str):
        e = embed.music_search_message(ctx, title=f"Searching for {query}..")
        msg = await ctx.send(embed=e)
        req: Request = Request(f"{source}{query}")
        await req.process()
        if not req.success:
            e = embed.music_not_found_message(
                ctx,
                title=f"Nothing found for {query}, sorry..",
            )
            await msg.edit(embed=e)
            return

        playlist: Playlist = Playlist.from_request(req)
        e = embed.playlist_message(ctx, title=f"Result for {query}", playlist=playlist)
        await msg.edit(embed=e)
        for i in range(1, len(playlist) + 1):
            await msg.add_reaction(f"{converter.number_to_emoji(i)}")
        await msg.add_reaction(_SearchReaction.CANCEL_REACTION)

        def check(reaction: Reaction, user: User):
            return (
                reaction.emoji in _SearchReaction.ALLOWED_REACTION
                and user == ctx.message.author
            )

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=check,
                timeout=float(os.environ["BOT_SEARCH_TIMEOUT"]),
            )
            await msg.clear_reactions()
            if reaction.emoji == _SearchReaction.CANCEL_REACTION:
                raise _SearchCanceledException
            await msg.add_reaction("👍")
            await msg.add_reaction(reaction.emoji)
        except (asyncio.TimeoutError, _SearchCanceledException):
            e = embed.music_search_message(ctx, title="Research canceled")
            await msg.clear_reactions()
            await msg.edit(embed=e)
            return

        song: Song = playlist[converter.emoji_to_number(reaction.emoji) - 1]
        e = embed.music_message(ctx, song)
        await msg.edit(embed=e)

        # PlayerContainer create bot if needed
        player: Player = self._players[ctx.guild.id]
        await player.play(ctx, song)
        await msg.clear_reactions()

    @commands.command(
        aliases=["sc", "ssc"],
        brief="search a song on SoundCloud",
        help="search a query on SoundCloud and display the 10 first result",
        usage="<query>",
    )
    @commands.guild_only()
    async def soundcloud(self, ctx: Context, *, query: str):
        await self._search_process(ctx, query, "scsearch:")

    @commands.command(
        aliases=["yt", "syt"],
        brief="search a song on YouTube",
        help="search a query on YouTube and display the 10 first result",
        usage="<query>",
    )
    @commands.guild_only()
    async def youtube(self, ctx: Context, *, query: str):
        await self._search_process(ctx, query, "ytsearch10:")


def setup(bot):
    bot.add_cog(Search(bot))


class _SearchCanceledException(Exception):
    pass


class _SearchReaction:
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