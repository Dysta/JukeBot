from typing import Optional

from nextcord import Embed
from nextcord.ext import commands
from nextcord.ext.commands import Bot, BucketType, Context

from jukebot.checks import user, voice
from jukebot.components import ResultSet, Player, Query, Result
from jukebot.exceptions import QueryFailed
from jukebot.utils import embed, regex


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.command(
        aliases=["queue", "q", "list"],
        brief="Show the queue of the server.",
        help="Show the queue of the server",
    )
    @commands.guild_only()
    @commands.cooldown(1, 3.0, BucketType.user)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def show(self, ctx: Context):
        queue: ResultSet = self.bot.players[ctx.guild.id].queue
        e: Embed = embed.queue_message(
            ctx.author, queue, title=f"Queue for {ctx.guild.name}"
        )
        await ctx.send(embed=e)

    @commands.command(
        aliases=["a"],
        brief="Add a song to the current queue.",
        help="Add a song to the current player queue",
        usage="<url|query_str>",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def add(
        self,
        ctx: Context,
        top: Optional[bool] = False,
        silent: Optional[bool] = False,
        *,
        query: str,
    ):
        query_str = query if regex.is_url(query) else f"ytsearch1:{query}"
        if not silent:
            ctx.typing()

        qry: Query = Query(query_str)
        await qry.search()
        if not qry.success:
            raise QueryFailed(
                f"Nothing found for {query}", query=query, full_query=query_str
            )

        if qry.type == Query.Type.PLAYLIST:
            res: ResultSet = ResultSet.from_query(qry, ctx.author)
            player: Player = self.bot.players[ctx.guild.id]
            if top:
                player.queue = res + player.queue
            else:
                player.queue += res

            e: Embed = embed.basic_queue_message(
                ctx.author, title=f"Enqueued : {len(res)} songs"
            )
            await ctx.send(embed=e)
        else:
            res: Result = Result.from_query(qry)
            res.requester = ctx.author
            player: Player = self.bot.players[ctx.guild.id]
            if top:
                player.queue.add(res)
            else:
                player.queue.put(res)
            if not silent and player.is_playing:
                e: Embed = embed.result_enqueued(ctx.author, res)
                await ctx.send(embed=e)
        return True

    @commands.command(
        aliases=["r"],
        brief="Remove a song from the current queue.",
        help="Remove the song at pos `idx` of the queue",
        usage="<idx>",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(user.bot_queue_is_not_empty)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def remove(self, ctx: Context, idx: int):
        queue: ResultSet = self.bot.players[ctx.guild.id].queue
        if not (elem := queue.remove(idx - 1)):
            raise commands.UserInputError(f"Can't delete item number {idx}")

        e: Embed = embed.basic_message(
            ctx.author, content=f"`{elem.title}` have been removed from the queue"
        )
        await ctx.send(embed=e)

    @commands.command(
        aliases=["clr"],
        brief="Clear the current queue.",
        help="Remove all the songs of the queue",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(user.bot_queue_is_not_empty)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    async def clear(self, ctx: Context):
        player: Player = self.bot.players[ctx.guild.id]
        player.queue = ResultSet.empty()

        e: Embed = embed.basic_message(ctx.author, title="The queue have been cleared.")
        await ctx.send(embed=e)

    @commands.command(
        aliases=["sfl"],
        brief="Shuffle the current queue.",
        help="Shuffle the current queue.",
    )
    @commands.guild_only()
    @commands.check(user.bot_queue_is_not_empty)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.guild)
    async def shuffle(self, ctx: Context):
        self.bot.players[ctx.guild.id].queue.shuffle()
        e: Embed = embed.basic_message(ctx.author, title="Queue shuffled.")
        await ctx.send(embed=e)

    @commands.command(
        name="qloop",
        aliases=["qlp"],
        brief="Loop the current queue.",
        help="Allow user to enable or disable the looping of the queue.",
    )
    @commands.guild_only()
    @commands.check(user.bot_queue_is_not_empty)
    @commands.check(voice.bot_and_user_in_same_channel)
    @commands.check(voice.bot_is_connected)
    @commands.check(voice.user_is_connected)
    @commands.cooldown(1, 5.0, BucketType.user)
    async def queue_loop(self, ctx: Context):
        player: Player = self.bot.players[ctx.guild.id]
        looping: bool = player.loop.is_queue_loop
        if looping:
            player.loop = Player.Loop.DISABLED
            new_status = "disabled"
        else:
            player.loop = Player.Loop.QUEUE
            new_status = "enabled"

        e: embed = embed.basic_message(ctx.author, title=f"Queue loop is {new_status}")
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Queue(bot))
