from nextcord import Permissions
from nextcord.ext import commands
from typing import Optional

from loguru import logger

from nextcord.ext.commands import Context, BucketType

from jukebot.utils import Extensions, embed


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _reload_all_cogs(self):
        logger.opt(lazy=True).info("Reloading all extensions.")
        for e in Extensions.all():
            self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
            logger.opt(lazy=True).success(
                f"Extension {e['package']}.{e['name']} reloaded."
            )
        logger.opt(lazy=True).info("All extensions have been successfully reloaded.")

    def _reload_cog(self, name):
        logger.opt(lazy=True).info(f"Reloading '{name}' extension.")
        e = Extensions.get(name)
        if e is None:
            logger.error(f"Extension {name!r} could not be loaded.")
            raise commands.ExtensionNotFound(name)
        self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
        logger.opt(lazy=True).success(f"Extension {e['package']}.{e['name']} reloaded.")

    @commands.command(
        aliases=["rld"],
        brief="Reload a cog or all cogs",
        help="Reload the given cog. If no cog is given, reload all cogs.",
        usage="reload [cogs_name]",
        hidden=True,
    )
    @commands.guild_only()
    @commands.is_owner()
    async def reload(self, ctx, cog_name: Optional[str] = None):
        try:
            if not cog_name:
                self._reload_all_cogs()
            else:
                self._reload_cog(cog_name)
        except Exception:
            await ctx.message.add_reaction("❌")
            raise
        await ctx.message.add_reaction("✅")

    @commands.command(
        aliases=["pfx"],
        brief="Change the prefix of the bot",
        help="Set a new prefix for the bot.\nIf no prefix are given, sends the current server prefix.",
        usage="[prefix]",
    )
    @commands.guild_only()
    @commands.cooldown(1, 15.0, BucketType.guild)
    async def prefix(self, ctx: Context, prefix: Optional[str] = None):
        if not prefix:
            e = embed.basic_message(
                ctx.author,
                content=f"Prefix for `{ctx.guild.name}` is `{await self.bot.prefixes.get_item(ctx.guild.id)}`",
            )
            await ctx.send(embed=e)
            return

        perm: Permissions = ctx.author.guild_permissions
        logger.opt(lazy=True).info(
            f"Set prefix '{prefix}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
        )
        if perm.administrator:
            await self.bot.prefixes.set_item(ctx.guild.id, prefix)
            e = embed.basic_message(
                ctx.author,
                title="Prefix changed!",
                content=f"Prefix is set to `{prefix}` for server `{ctx.guild.name}`",
            )
            logger.opt(lazy=True).success(
                f"Successfully set prefix '{prefix}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
            )
        else:
            e = embed.error_message(
                ctx.author, content="You're not administrator of this server."
            )
            logger.opt(lazy=True).error(
                f"Missing permission for setting prefix '{prefix}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
            )
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(System(bot))
