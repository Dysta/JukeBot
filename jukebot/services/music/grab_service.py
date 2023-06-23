from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import CommandInteraction, Forbidden

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import AudioStream, Player, Song


class GrabService(AbstractService):
    async def __call__(self, /, interaction: CommandInteraction):
        player: Player = self.bot.players[interaction.guild.id]
        stream: AudioStream = player.stream
        song: Song = player.song
        e = embed.grab_message(song, stream.progress)
        e.add_field(
            name="Voice channel",
            value=f"`{interaction.guild.name} — {interaction.author.voice.channel.name}`",
        )
        try:
            await interaction.author.send(embed=e)
            await interaction.send("Saved!", ephemeral=True)
        except Forbidden:
            await interaction.send("Your DMs are closed!", embed=e, ephemeral=True)
