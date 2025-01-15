from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction, Embed
from disnake.ext import commands
from disnake.ext.commands import BucketType

from jukebot import JukeBot
from jukebot.components.requests.music_request import MusicRequest
from jukebot.services.queue import (
    AddService,
    ClearService,
    RemoveService,
    ShowService,
    ShuffleService,
)
from jukebot.utils import checks, embed

if TYPE_CHECKING:
    from jukebot.components import Result, ResultSet


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot: JukeBot = bot

    @commands.slash_command()
    async def queue(self, inter: CommandInteraction):
        """Base command to perform manipulations on the bot queue

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """

    @queue.sub_command()
    @commands.cooldown(1, 3.0, BucketType.user)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def show(self, inter: CommandInteraction):
        """Shows queue, music count and total duration

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        queue: ResultSet = await self.bot.services.show(guild_id=inter.guild.id)

        e: Embed = embed.queue_message(queue, self.bot, title=f"Queue for {inter.guild.name}")
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
        """Add a song to the current queue

        Parameters
        ----------
        inter: The interaction
        query: the URL or query to play
        top: Whether or not to put music at the top of the queue
        """
        if not inter.response.is_done():
            await inter.response.defer()

        type, res = await self.bot.services.add(guild_id=inter.guild.id, author=inter.author, query=query, top=top)

        if type == MusicRequest.ResultType.PLAYLIST:
            e: Embed = embed.basic_queue_message(content=f"Enqueued : {len(res)} songs")
        else:
            e: Embed = embed.result_enqueued(res)
        await inter.edit_original_message(embed=e)

    @queue.sub_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_queue_is_not_empty)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def clear(self, inter: CommandInteraction):
        """Remove all music from the current queue

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        await self.bot.services.clear(guild_id=inter.guild.id)

        e: Embed = embed.basic_message(title="The queue have been cleared.")
        await inter.send(embed=e)

    @queue.sub_command()
    @commands.check(checks.bot_queue_is_not_empty)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    @commands.cooldown(1, 10.0, BucketType.guild)
    async def shuffle(self, inter: CommandInteraction):
        """Shuffles the current queue

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        await self.bot.services.shuffle(guild_id=inter.guild.id)

        e: Embed = embed.basic_message(title="Queue shuffled.")
        await inter.send(embed=e)

    @queue.sub_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.check(checks.bot_queue_is_not_empty)
    @commands.check(checks.bot_and_user_in_same_channel)
    @commands.check(checks.bot_is_connected)
    @commands.check(checks.user_is_connected)
    async def remove(self, inter: CommandInteraction, song: str):
        """Remove a song from the queue

        Parameters
        ----------
        inter: The interaction
        song: The name of the music to remove. The bot auto completes the answer
        """
        elem: Result = await self.bot.services.remove(guild_id=inter.guild.id, song=song)

        e: Embed = embed.basic_message(content=f"`{elem.title}` have been removed from the queue")
        await inter.send(embed=e)

    @remove.autocomplete("song")
    async def remove_autocomplete(self, inter: CommandInteraction, data: str):
        data = data.lower()
        queue: ResultSet = self.bot.players[inter.guild.id].queue
        return [e.title for e in queue if data in e.title.lower()][:25]


def setup(bot: JukeBot):
    bot.add_cog(Queue(bot))

    bot.add_service(AddService(bot))
    bot.add_service(ClearService(bot))
    bot.add_service(RemoveService(bot))
    bot.add_service(ShuffleService(bot))
    bot.add_service(ShowService(bot))
