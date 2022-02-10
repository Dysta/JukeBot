from loguru import logger
from nextcord.ext import commands
from nextcord.ext.commands import Context, Command


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
            f"parameters: '{ctx.args}' - '{ctx.kwargs}' | "
            f"raw message: '{ctx.message.content}'."
        )

    @commands.Cog.listener()
    async def on_command_invoked(self, ctx: Context, cmd: Command):
        logger.opt(lazy=True).info(
            f"Server: '{ctx.guild.name}' (ID: {ctx.guild.id}) | "
            f"Channel: '{ctx.channel.name}' (ID: {ctx.channel.id}) | "
            f"Invoker: '{ctx.author}' | "
            f"command: '{ctx.command.cog.qualified_name if ctx.command else 'None'}:{ctx.command.name if ctx.command else 'None'} | "
            f"parameters: '{ctx.args}' - '{ctx.kwargs}' | "
            f"invoked command: '{cmd.cog.qualified_name}:{cmd.name}' | "
            f"raw message: '{ctx.message.content}'."
        )


def setup(bot):
    bot.add_cog(LoggerHandler(bot))
