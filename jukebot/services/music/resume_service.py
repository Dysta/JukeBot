from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import APISlashCommand, CommandInteraction

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

            return

        if player.state.is_stopped and not player.queue.is_empty():
            with PlayService(self.bot) as play:
                await play(interaction=interaction, query="")
            return

        cmd: APISlashCommand = self.bot.get_global_command_named("play")
        e = embed.basic_message(title="Nothing is currently playing", content=f"Try </play:{cmd.id}> to add a music !")
        await interaction.send(embed=e)
