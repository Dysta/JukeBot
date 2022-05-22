from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction, Embed
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from jukebot.services.queue import (
    AddService,
    ClearService,
    RemoveService,
    ShuffleService,
)
from jukebot.utils import checks, embed

if TYPE_CHECKING:
    from jukebot.components import ResultSet


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command(description="Manipulate the queue of the player.")
    async def queue(self, inter: CommandInteraction):
        pass

    @queue.sub_command(
        description="Show the queue of the server",
    )
    @commands.cooldown(1, 3.0, BucketType.user)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def show(self, inter: CommandInteraction):
        queue: ResultSet = self.bot.players[inter.guild.id].queue
        e: Embed = embed.queue_message(
            inter.author, queue, title=f"Queue for {inter.guild.name}"
        )
        await inter.send(embed=e)

    @queue.sub_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def add(
        self,
        inter: CommandInteraction,
        query: str,
        top: Optional[bool] = False,
    ):
        """
        Add a song to the current queue
        Parameters
        ----------
        inter: The interaction
        query: the URL or query to play
        top: Put the requested song at the top of the queue

        Returns
        -------

        """
        with AddService(self.bot) as asr:
            await asr(interaction=inter, query=query, top=top)

    @queue.sub_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_queue_is_not_empty)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def remove(self, inter: CommandInteraction, song: str):
        """
        Remove a song from the queue
        Parameters
        ----------
        inter: The interaction
        song: The song to remove

        Returns
        -------

        """
        with RemoveService(self.bot) as rs:
            await rs(interaction=inter, song=song)  # type:ignore

    @remove.autocomplete("song")
    async def remove_autocomplete(self, inter: CommandInteraction, data: str):
        data = data.lower()
        queue: ResultSet = self.bot.players[inter.guild.id].queue
        return [e.title for e in queue if data in e.title.lower()][:25]

    @queue.sub_command(
        description="Remove all the songs of the queue",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_queue_is_not_empty)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def clear(self, inter: CommandInteraction):
        with ClearService(self.bot) as cs:
            await cs(interaction=inter)

    @queue.sub_command(
        description="Shuffle the current queue.",
    )
    @commands.check(checks.bot_queue_is_not_empty)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.guild)
    async def shuffle(self, inter: CommandInteraction):
        with ShuffleService(self.bot) as ss:
            await ss(interaction=inter)


def setup(bot):
    bot.add_cog(Queue(bot))
