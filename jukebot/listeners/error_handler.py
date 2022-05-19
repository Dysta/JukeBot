from __future__ import annotations

from disnake import CommandInteraction, Embed
from disnake.ext import commands
from disnake.ext.commands import CommandError, Context
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
            e: Embed = embed.info_message(
                ctx.author,
                content="`JukeBot` has migrated its commands to slash commands, the new prefix is `/`.\n"
                "If the commands don't appear, **kick and re-invite** JukeBot in your server using this link: "
                "https://dsc.gg/jukebot",
            )
            await ctx.reply(embed=e)
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

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: CommandInteraction, error: CommandError
    ):
        logger.opt(lazy=True).error(error)
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, exceptions.QueryException):
            logger.opt(lazy=True).warning(
                f"Query Exception [{error.__class__.__name__}] '{error.query}' ({error.full_query}) for guild '{inter.guild.name} (ID: {inter.guild.id})'."
            )
            e = embed.music_not_found_message(
                inter.author,
                title=error,
            )
            if inter.response.is_done():
                await inter.edit_original_message(embed=e)
            else:
                await inter.send(embed=e, ephemeral=True)
            return

        e = embed.error_message(inter.author, content=error)
        if inter.response.is_done():
            await inter.edit_original_message(embed=e)
        else:
            await inter.send(embed=e, ephemeral=True)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
