from __future__ import annotations

from typing import TYPE_CHECKING

from disnake.ext import commands
from loguru import logger

from jukebot import exceptions
from jukebot.views.embed import error_message, music_not_found_message

if TYPE_CHECKING:
    from disnake import CommandInteraction
    from disnake.ext.commands import CommandError


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: CommandInteraction, error: CommandError):
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, exceptions.QueryException):
            logger.opt(lazy=True).warning(
                f"Query Exception [{error.__class__.__name__}] '{error.query}' ({error.full_query}) for guild '{inter.guild.name} (ID: {inter.guild.id})'."
            )
            e = music_not_found_message(
                title=error,
            )
            if inter.response.is_done():
                await inter.edit_original_message(embed=e)
            else:
                await inter.send(embed=e, ephemeral=True)
            return

        e = error_message(content=error)
        if inter.response.is_done():
            await inter.edit_original_message(embed=e)
        else:
            await inter.send(embed=e, ephemeral=True)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
