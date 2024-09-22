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
        # PlayerContainer create bot if needed
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
            return True

        rqs: Result = player.queue.get()
        author = rqs.requester
        async with StreamRequest(rqs.web_url) as req:
            await req.execute()

        song: Song = components.Song(req.result)
        song.requester = author

        for i in range(2):
            if await self._try_to_play(interaction, player, song, i):
                break

            with ResetService(self.bot) as reset, JoinService(self.bot) as join:
                await reset(guild=interaction.guild)
                logger.opt(lazy=True).info(f"Server {interaction.guild.name} ({interaction.guild.id}) player reset.")

                await join(interaction=interaction)
                logger.opt(lazy=True).info(
                    f"Server {interaction.guild.name} ({interaction.guild.id}) player connected."
                )

        else:
            with ResetService(self.bot) as reset:
                await reset(guild=interaction.guild)
            logger.opt(lazy=True).error(
                f"Server {interaction.guild.name} ({interaction.guild.id}) can't play in its player after 2 attempts. "
                f"Shouldn't happen."
            )
            raise PlayerConnexionException(
                "The player cannot play on the voice channel. This is because he's not connected to a voice channel or he's already playing something.\n"
                "This situation can happen when the player has been abruptly disconnected by Discord or a user. "
                "Use the `reset` command to reset the player in this case."
            )

        logger.opt(lazy=True).success(
            f"Server {interaction.guild.name} ({interaction.guild.id}) can play in its player."
        )

        return song, player.loop

    async def _try_to_play(self, interaction: CommandInteraction, player: Player, song: Song, attempt: int) -> bool:
        """
        An asynchronous function to attempt to play a song in a Discord guild.

        Parameters
        ----------
        interaction : CommandInteraction
            The command interaction triggering the play attempt.
        player : Player
            The player responsible for playing the song.
        song : Song
            The song to be played.
        attempt : int
            The attempt number for playing the song.

        Returns
        -------
        bool
            True if the song was played successfully, False otherwise.
        """
        logger.opt(lazy=True).info(
            f"Attempt {attempt} to play in guild {interaction.guild.name} ({interaction.guild.id})"
        )
        try:
            await player.play(song)
        except Exception as e:
            logger.opt(lazy=True).error(
                f"Server {interaction.guild.name} ({interaction.guild.id}) can't play in its player at attempt {attempt}. Err {e}"
            )
            return False
        return True
