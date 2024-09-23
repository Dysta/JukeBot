from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import Member

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.components.requests.music_request import MusicRequest
from jukebot.exceptions import QueryFailed

if TYPE_CHECKING:
    from jukebot.components import Player, Result, ResultSet


class AddService(AbstractService):
    async def __call__(
        self,
        /,
        guild_id: int,
        author: Member,
        query: str,
        top: Optional[bool] = False,
    ):
        async with MusicRequest(query) as req:
            await req.execute()

        if not req.success:
            raise QueryFailed(f"Nothing found for {query}", query=query, full_query=query)

        if req.type == MusicRequest.ResultType.PLAYLIST:
            res: ResultSet = components.ResultSet.from_result(req.result, author)
            player: Player = self.bot.players[guild_id]
        else:
            res: Result = components.Result(req.result)
            res.requester = author
            player: Player = self.bot.players[guild_id]

        if top:
            player.queue.add(res)
        else:
            player.queue.put(res)

        return req.type, res
