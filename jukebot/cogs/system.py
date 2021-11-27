from nextcord import Permissions
from nextcord.ext import commands
from typing import Optional

from nextcord.ext.commands import Context, BucketType

from jukebot.utils import Extensions, embed


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _reload_all_cogs(self):
        for e in Extensions.all():
            try:
                self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
            except commands.ExtensionNotFound as e:
                print(e)
                raise e

    def _reload_cog(self, name):
        e = Extensions.get(name)
        if e is None:
            raise commands.ExtensionNotFound(name)

        try:
            self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
            return
        except commands.ExtensionNotFound as e:
            print(e)
            raise e

    @commands.command(
        aliases=["rld"],
        brief="Reload a cog or all cogs",
        help="Reload the given cog. If no cog is given, reload all cogs.",
        usage="reload [cogs_name]",
        hidden=True,
    )
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, cog_name: Optional[str] = None):
        try:
            if cog_name is None:
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
        if prefix:
            perm: Permissions = ctx.author.guild_permissions
            if perm.administrator:
                await self.bot.set_prefix_for(str(ctx.guild.id), prefix)
                e = embed.basic_message(
                    ctx,
                    title="Prefix changed!",
                    content=f"Prefix is set to `{prefix}` for server `{ctx.guild.name}`",
                )
            else:
                e = embed.error_message(ctx, title="You're not administrator of this server.")
            await ctx.send(embed=e)
        else:
            e = embed.basic_message(
                ctx,
                content=f"Prefix for `{ctx.guild.name}` is `{self.bot.prefixes[str(ctx.guild.id)]}`",
            )
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(System(bot))
