from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from disnake import CommandInteraction, Embed
from loguru import logger

from jukebot import components
from jukebot.abstract_components import AbstractService
from jukebot.components.requests import StreamRequest
from jukebot.services import ResetService
from jukebot.services.music.join_service import JoinService
from jukebot.services.queue.add_service import AddService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import Player, Result, Song


class PlayService(AbstractService):
    async def __call__(
        self,
        /,
        query: str,
        top: Optional[bool] = False,
        silent: Optional[bool] = False,
    ):
        if not self.interaction.response.is_done():
            await self.interaction.response.defer()

        # PlayerContainer create bot if needed
        player: Player = self.bot.players[self.interaction.guild.id]

        if not player.is_connected:
            async with JoinService(self.bot, self.interaction) as join:
                if not await join(silent=True):
                    return False

        if query:
            async with AddService(self.bot, self.interaction) as add:
                ok = await add(
                    query=query,
                    silent=silent or not player.is_playing,
                )
                if not ok:
                    return False

        if player.is_playing:
            return True  # return True bc everything is ok

        rqs: Result = player.queue.get()
        author = rqs.requester
        async with StreamRequest(rqs.web_url) as req:
            await req()

        song: Song = components.Song(req.result)
        song.requester = author

        for i in range(2):
            if await self._try_to_play(self.interaction, player, song, i):
                break

            async with ResetService(self.bot, self.interaction) as reset, JoinService(
                self.bot, self.interaction
            ) as join:
                await reset(silent=True)
                logger.opt(lazy=True).info(
                    f"Server {self.interaction.guild.name} ({self.interaction.guild.id}) player reset."
                )
                await join(silent=True)
                logger.opt(lazy=True).info(
                    f"Server {self.interaction.guild.name} ({self.interaction.guild.id}) player connected."
                )

        else:
            async with ResetService(self.bot, self.interaction) as reset:
                await reset(silent=True)
            logger.opt(lazy=True).error(
                f"Server {self.interaction.guild.name} ({self.interaction.guild.id}) can't play in its player after 2 attempts. "
                f"Shouldn't happen."
            )
            e: Embed = embed.error_message(
                content="The player cannot play on the voice channel. This is because he's not connected to a voice channel or he's already playing something.\n"
                "This situation can happen when the player has been abruptly disconnected by Discord or a user. "
                "Use the `reset` command to reset the player in this case.",
            )
            await self.interaction.edit_original_message(embed=e)
            return False

        logger.opt(lazy=True).success(
            f"Server {self.interaction.guild.name} ({self.interaction.guild.id}) can play in its player."
        )
        e: Embed = embed.music_message(song)
        await self.interaction.edit_original_message(embed=e)
        return True

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
