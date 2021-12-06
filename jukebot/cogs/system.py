from nextcord import Permissions
from nextcord.ext import commands
from typing import Optional

from nextcord.ext.commands import Context, BucketType

from jukebot.checks import user
from jukebot.utils import Extensions, embed


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _reload_all_cogs(self):
        for e in Extensions.all():
            self.bot.reload_extension(name=f"{e['package']}.{e['name']}")

    def _reload_cog(self, name):
        e = Extensions.get(name)
        if e is None:
            raise commands.ExtensionNotFound(name)
        self.bot.reload_extension(name=f"{e['package']}.{e['name']}")

    @commands.command(
        aliases=["rld"],
        brief="Reload a cog or all cogs",
        help="Reload the given cog. If no cog is given, reload all cogs.",
        usage="reload [cogs_name]",
        hidden=True,
    )
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.check(user.is_dysta)
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
        if perm.administrator:
            await self.bot.prefixes.set_item(ctx.guild.id, prefix)
            e = embed.basic_message(
                ctx.author,
                title="Prefix changed!",
                content=f"Prefix is set to `{prefix}` for server `{ctx.guild.name}`",
            )
        else:
            e = embed.error_message(
                ctx.author, content="You're not administrator of this server."
            )
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(System(bot))
