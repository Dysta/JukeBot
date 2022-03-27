from nextcord.ext import commands
from nextcord.ext.commands import Context, CommandError

from loguru import logger

from jukebot import exceptions
from jukebot.utils import embed


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        logger.opt(lazy=True).error(error)
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("⁉")
            return

        if isinstance(error, exceptions.QueryException):
            logger.opt(lazy=True).warning(
                f"Query Exception [{error.__class__.__name__}] '{error.query}' ({error.full_query}) for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
            )
            e = embed.music_not_found_message(
                ctx.author,
                title=error,
            )
            await ctx.send(embed=e, delete_after=5.0)
            return

        e = embed.error_message(ctx.author, content=error)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
