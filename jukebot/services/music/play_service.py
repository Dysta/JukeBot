from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction
from loguru import logger

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.components.requests import StreamRequest
from jukebot.exceptions.player_exception import PlayerConnexionException
from jukebot.services import ResetService
from jukebot.services.music.join_service import JoinService
from jukebot.services.queue.add_service import AddService

if TYPE_CHECKING:
    from jukebot.components import Player, Result, Song


class PlayService(AbstractService):
    async def __call__(
        self,
        /,
        interaction: CommandInteraction,
        query: str,
        top: Optional[bool] = False,
    ):
        player: Player = self.bot.players[interaction.guild.id]

        if not player.is_connected:
            with JoinService(self.bot) as join:
                await join(interaction=interaction)

        if query:
            with AddService(self.bot) as add:
                await add(
                    guild_id=interaction.guild.id,
                    author=interaction.user,
                    query=query,
                    top=top,
                )

        if player.is_playing:
            # ? stop here cause it mean that we used play command as queue add command
            return

        rqs: Result = player.queue.get()
        author = rqs.requester
        async with StreamRequest(rqs.web_url) as req:
            await req.execute()

        song: Song = components.Song(req.result)
        song.requester = author

        try:
            await player.play(song)
        except Exception as e:
            logger.opt(lazy=True).error(
                f"Server {interaction.guild.name} ({interaction.guild.id}) can't play in its player. Err {e}"
            )

            cmd = self.bot.get_global_command_named("reset")
            raise PlayerConnexionException(
                "The player cannot play on the voice channel. This is because he's not connected to a voice channel or he's already playing something.\n"
                "This situation can happen when the player has been abruptly disconnected by Discord or a user (kicked from a voice channel). "
                f"Use the </reset:{cmd.id}> command to reset the player in this case."
            )

        logger.opt(lazy=True).success(
            f"Server {interaction.guild.name} ({interaction.guild.id}) can play in its player."
        )

        return song, player.loop
