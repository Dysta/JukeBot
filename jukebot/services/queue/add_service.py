from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction, Embed

from jukebot import components
from jukebot.abstract_components import AbstractService
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
        query_str = query if regex.is_url(query) else f"ytsearch1:{query}"
        if not interaction.response.is_done():
            await interaction.response.defer()

        qry: Query = components.Query(query_str)
        await qry.search()
        if not qry.success:
            raise QueryFailed(f"Nothing found for {query}", query=query, full_query=query_str)

        if qry.type == components.Query.Type.PLAYLIST:
            res: ResultSet = components.ResultSet.from_query(qry, interaction.author)
            player: Player = self.bot.players[interaction.guild.id]
            if top:
                player.queue = res + player.queue
            else:
                player.queue += res

            e: Embed = embed.basic_queue_message(
                interaction.author, title=f"Enqueued : {len(res)} songs"
            )
            await interaction.edit_original_message(embed=e)
        else:
            res: Result = components.Result.from_query(qry)
            res.requester = interaction.author
            player: Player = self.bot.players[interaction.guild.id]
            if top:
                player.queue.add(res)
            else:
                player.queue.put(res)
            if not silent:
                e: Embed = embed.result_enqueued(interaction.author, res)
                await interaction.edit_original_message(embed=e)
        return True
