from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import Forbidden

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import AudioStream, Player, Song


class GrabService(AbstractService):
    async def __call__(self):
        player: Player = self.bot.players[self.interaction.guild.id]
        stream: AudioStream = player.stream
        song: Song = player.song
        e = embed.grab_message(song, stream.progress)
        e.add_field(
            name="Voice channel",
            value=f"`{self.interaction.guild.name} — {self.interaction.author.voice.channel.name}`",
        )
        try:
            await self.interaction.author.send(embed=e)
            await self.interaction.send("Saved!", ephemeral=True)
        except Forbidden:
            await self.interaction.send("Your DMs are closed!", embed=e, ephemeral=True)
