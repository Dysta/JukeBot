from __future__ import annotations

import traceback

from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import CommandError
from loguru import logger


def fancy_traceback(exc: Exception) -> str:
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


class LoggerHandler(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_slash_command(self, inter: CommandInteraction):
        logger.opt(lazy=True).info(
            f"Server: '{inter.guild.name}' (ID: {inter.guild.id}) | "
            f"Channel: '{inter.channel.name}' (ID: {inter.channel.id}) | "
            f"Invoker: '{inter.author}' | "
            f"Command: '{inter.application_command.cog.qualified_name}:{inter.application_command.name}' | "
            f"raw options: '{inter.options}'."
        )

    @commands.Cog.listener()
    async def on_slash_command_completion(self, inter: CommandInteraction):
        logger.opt(lazy=True).success(
            f"Server: '{inter.guild.name}' (ID: {inter.guild.id}) | "
            f"Channel: '{inter.channel.name}' (ID: {inter.channel.id}) | "
            f"Invoker: '{inter.author}' | "
            f"Command: '{inter.application_command.cog.qualified_name}:{inter.application_command.name}' | "
            f"raw options: '{inter.options}'."
        )

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: CommandInteraction, error: CommandError):
        logger.error(
            f"Server: '{inter.guild.name}' (ID: {inter.guild.id}) | "
            f"Channel: '{inter.channel.name}' (ID: {inter.channel.id}) | "
            f"Invoker: '{inter.author}' | "
            f"Command: '{inter.application_command.cog.qualified_name}:{inter.application_command.name}' | "
            f"raw options: '{inter.options}' | "
            f"error: {error} | \n"
            f"traceback : {fancy_traceback(error)}"
        )


def setup(bot):
    bot.add_cog(LoggerHandler(bot))
