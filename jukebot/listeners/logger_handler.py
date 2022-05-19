from __future__ import annotations

from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Command, Context
from loguru import logger


class LoggerHandler(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: Context):
        logger.opt(lazy=True).info(
            f"Server: '{ctx.guild.name}' (ID: {ctx.guild.id}) | "
            f"Channel: '{ctx.channel.name}' (ID: {ctx.channel.id}) | "
            f"Invoker: '{ctx.author}' | "
            f"command: '{ctx.command.cog.qualified_name}:{ctx.command.name}' | "
            f"raw message: '{ctx.message.content}'."
        )

    @commands.Cog.listener()
    async def on_command_invoked(self, ctx: Context, cmd: Command):
        logger.opt(lazy=True).info(
            f"Server: '{ctx.guild.name}' (ID: {ctx.guild.id}) | "
            f"Channel: '{ctx.channel.name}' (ID: {ctx.channel.id}) | "
            f"Invoker: '{ctx.author}' | "
            f"command: '{ctx.command.cog.qualified_name if ctx.command else 'None'}:{ctx.command.name if ctx.command else 'None'} | "
            f"invoked command: '{cmd.cog.qualified_name}:{cmd.name}' | "
            f"raw message: '{ctx.message.content}'."
        )

    @commands.Cog.listener()
    async def on_slash_command(self, inter: CommandInteraction):
        logger.opt(lazy=True).info(
            f"Server: '{inter.guild.name}' (ID: {inter.guild.id}) | "
            f"Channel: '{inter.channel.name}' (ID: {inter.channel.id}) | "
            f"Invoker: '{inter.author}' | "
            f"Command: '{inter.application_command.cog.qualified_name}:{inter.application_command.name}' | "
            f"raw options: '{inter.options}'."
        )


def setup(bot):
    bot.add_cog(LoggerHandler(bot))
