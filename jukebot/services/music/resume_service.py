from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

from .play_service import PlayService

if TYPE_CHECKING:
    from jukebot.components import Player


class ResumeService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction, silent: Optional[bool] = False):
        player: Player = self.bot.players[interaction.guild.id]
        if player.is_paused:
            player.resume()
            if not silent:
                e = embed.basic_message(title="Player resumed")
                await interaction.send(embed=e)
        elif player.state.is_stopped and not player.queue.is_empty():
            with PlayService(self.bot) as play:
                await play(interaction=interaction, query="")
        else:
            e = embed.basic_message(title="Nothing to play", content=f"Try `/play` to add a music !")
            await interaction.send(embed=e)
