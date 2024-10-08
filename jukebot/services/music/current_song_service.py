from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import CommandInteraction

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import AudioStream, Player, Song


class CurrentSongService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction):
        player: Player = self.bot.players[interaction.guild.id]
        stream: AudioStream = player.stream
        song: Song = player.song
        if stream and song:
            e = embed.music_message(song, player.loop, stream.progress)
        else:
            cmd: APISlashCommand = self.bot.get_global_command_named("play")
            e = embed.basic_message(
                title="Nothing is currently playing", content=f"Try </play:{cmd.id}> to add a music !"
            )
        await interaction.send(embed=e)
