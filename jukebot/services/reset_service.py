from typing import TYPE_CHECKING, Optional

from disnake import Embed
from loguru import logger

from jukebot.abstract_components import AbstractService
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import Player


class ResetService(AbstractService):
    async def __call__(self, /, silent: Optional[bool] = False):
        if not self.interaction.guild.id in self.bot.players:
            logger.opt(lazy=True).debug(
                f"Server {self.interaction.guild.name} ({self.interaction.guild.id}) try to kill a player that don't exist."
            )
            if not silent:
                e: Embed = embed.error_message(content="No player detected in this server.")
                await self.interaction.send(embed=e, ephemeral=True)
            return

        player: Player = self.bot.players.pop(self.interaction.guild.id)
        try:
            await player.disconnect(force=True)
        except Exception as e:
            logger.opt(lazy=True).error(
                f"Error when force disconnecting the player of the guild {self.interaction.guild.name} ({self.interaction.guild.id}). "
                f"Error: {e}"
            )

        logger.opt(lazy=True).success(
            f"Server {self.interaction.guild.name} ({self.interaction.guild.id}) has successfully reset his player."
        )
        if not silent:
            e: Embed = embed.info_message(content="The player has been reset.")
            await self.interaction.send(embed=e)
