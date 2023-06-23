from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction, Embed

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.components.requests.music_request import MusicRequest
from jukebot.exceptions import QueryFailed
from jukebot.utils import embed, regex

if TYPE_CHECKING:
    from jukebot.components import Player, Query, Result, ResultSet


class AddService(AbstractService):
    async def __call__(
        self,
        /,
        interaction: CommandInteraction,
        query: str,
        top: Optional[bool] = False,
        silent: Optional[bool] = False,
    ):
        if not interaction.response.is_done():
            await interaction.response.defer()

        async with MusicRequest(query) as req:
            await req.execute()
        if not req.success:
            raise QueryFailed(f"Nothing found for {query}", query=query, full_query=query)

        if req.type == MusicRequest.ResultType.PLAYLIST:
            res: ResultSet = components.ResultSet.from_result(req.result, interaction.author)
            player: Player = self.bot.players[interaction.guild.id]
            if top:
                player.queue = res + player.queue
            else:
                player.queue += res

            e: Embed = embed.basic_queue_message(title=f"Enqueued : {len(res)} songs")
            await interaction.edit_original_message(embed=e)
        else:
            res: Result = components.Result(req.result)
            res.requester = interaction.author
            player: Player = self.bot.players[interaction.guild.id]
            if top:
                player.queue.add(res)
            else:
                player.queue.put(res)
            if not silent:
                e: Embed = embed.result_enqueued(res)
                await interaction.edit_original_message(embed=e)
        return True
