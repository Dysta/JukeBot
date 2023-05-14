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
            e = embed.music_message(song.requester, song=song, current_duration=stream.progress)
        else:
            e = embed.basic_message(
                interaction.author,
                title="Nothing is currently playing",
                content=f"Try `/play` to add a music !",
            )
        await interaction.send(embed=e)
