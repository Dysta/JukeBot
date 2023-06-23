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
        async with StreamRequest(rqs.web_url) as req:
            await req.execute()

        song: Song = components.Song(req.result)
        song.requester = author

        async def inner(attempt: int) -> bool:
            logger.opt(lazy=True).info(
                f"Attempt {attempt} to play in guild {interaction.guild.name} ({interaction.guild.id})"
            )
            try:
                await player.play(song)
            except:
                logger.opt(lazy=True).error(
                    f"Server {interaction.guild.name} ({interaction.guild.id}) can't play in its player at attempt {attempt}."
                )
                return False
            return True

        for i in range(2):
            if not await inner(i):
                with ResetService(self.bot) as rs, JoinService(self.bot) as js:
                    await rs(interaction=interaction, silent=True)
                    logger.opt(lazy=True).info(
                        f"Server {interaction.guild.name} ({interaction.guild.id}) player reset."
                    )
                    await js(interaction=interaction, silent=True)
                    logger.opt(lazy=True).info(
                        f"Server {interaction.guild.name} ({interaction.guild.id}) player connected."
                    )
            else:
                break
        else:
            with ResetService(self.bot) as rs:
                await rs(interaction=interaction, silent=True)
            logger.opt(lazy=True).error(
                f"Server {interaction.guild.name} ({interaction.guild.id}) can't play in its player after 2 attempts. "
                f"Shouldn't happen."
            )
            e: Embed = embed.error_message(
                content="The player cannot play on the voice channel. This is because he's not connected to a voice channel or he's already playing something.\n"
                "This situation can happen when the player has been abruptly disconnected by Discord or a user. "
                "Use the `reset` command to reset the player in this case.",
            )
            await interaction.edit_original_message(embed=e)
            return False

        logger.opt(lazy=True).success(
            f"Server {interaction.guild.name} ({interaction.guild.id}) can play in its player."
        )
        e: Embed = embed.music_message(song)
        await interaction.edit_original_message(embed=e)
        return True
