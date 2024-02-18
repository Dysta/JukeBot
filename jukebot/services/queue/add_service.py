from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import Embed

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.components.requests.music_request import MusicRequest
from jukebot.exceptions import QueryFailed
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import Player, Result, ResultSet


class AddService(AbstractService):
    async def __call__(
        self,
        /,
        query: str,
        top: Optional[bool] = False,
        silent: Optional[bool] = False,
    ):
        if not self.interaction.response.is_done():
            await self.interaction.response.defer()

        async with MusicRequest(query) as req:
            await req()
        if not req.success:
            raise QueryFailed(f"Nothing found for {query}", query=query, full_query=query)

        if req.type == MusicRequest.ResultType.PLAYLIST:
            res: ResultSet = components.ResultSet.from_result(req.result, self.interaction.author)
            player: Player = self.bot.players[self.interaction.guild.id]
            if top:
                player.queue = res + player.queue
            else:
                player.queue += res

            e: Embed = embed.basic_queue_message(title=f"Enqueued : {len(res)} songs")
            await self.interaction.edit_original_message(embed=e)
        else:
            res: Result = components.Result(req.result)
            res.requester = self.interaction.author
            player: Player = self.bot.players[self.interaction.guild.id]
            if top:
                player.queue.add(res)
            else:
                player.queue.put(res)
            if not silent:
                e: Embed = embed.result_enqueued(res)
                await self.interaction.edit_original_message(embed=e)
        return True
