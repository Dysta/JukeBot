from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction, Embed
from loguru import logger

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

from ..queue.add_service import AddService
from .join_service import JoinService

if TYPE_CHECKING:
    from jukebot.components import Player, Query, Result, Song


class PlayService(AbstractService):
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

        # PlayerContainer create bot if needed
        player: Player = self.bot.players[interaction.guild.id]

        if not player.is_connected:
            with JoinService(self.bot) as js:
                if not await js(interaction=interaction, silent=True):
                    return False

        if query:
            with AddService(self.bot) as asr:
                ok = await asr(
                    interaction=interaction,
                    query=query,
                    silent=silent or not player.is_playing,
                )
                if not ok:
                    return False

        if player.is_playing:
            return True  # return True bc everything is ok

        rqs: Result = player.queue.get()
        author = rqs.requester
        qry: Query = components.Query(rqs.web_url)
        await qry.process()

        song: Song = components.Song.from_query(qry)
        song.requester = author

        try:
            await player.play(song)
        except Exception as e:
            logger.opt(lazy=True).error(
                f"Server {interaction.guild.name} ({interaction.guild.id}) can't play in its player. Should not happen.\n"
                f"Error: {e}"
            )
            e: Embed = embed.error_message(
                author,
                content="The player cannot play on the voice channel. This is because he's not connected to a voice channel or he's already playing something.\n"
                "This situation can happen when the player has been abruptly disconnected by Discord or a user. "
                "Use the `reset` command to reset the player in this case.",
            )
            await interaction.edit_original_message(embed=e)
            return False

        e: Embed = embed.music_message(author, song)
        await interaction.edit_original_message(embed=e)
        return True
