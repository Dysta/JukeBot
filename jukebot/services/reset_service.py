from typing import TYPE_CHECKING

from disnake import Guild
from loguru import logger

from jukebot.abstract_components import AbstractService
from jukebot.exceptions.player_exception import PlayerDontExistException

if TYPE_CHECKING:
    from jukebot.components import Player


class ResetService(AbstractService):
    async def __call__(self, /, guild: Guild):
        if not guild.id in self.bot.players:
            logger.opt(lazy=True).debug(f"Server {guild.name} ({guild.id}) try to kill a player that don't exist.")
            raise PlayerDontExistException("No player detected in this server.")

        player: Player = self.bot.players.pop(guild.id)
        try:
            await player.disconnect(force=True)
        except Exception as e:
            logger.opt(lazy=True).error(
                f"Error when force disconnecting the player of the guild {guild.name} ({guild.id}). " f"Error: {e}"
            )

        logger.opt(lazy=True).success(f"Server {guild.name} ({guild.id}) has successfully reset his player.")
