from discord.ext import commands
from typing import Optional
from extensions import Extensions


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
        usage="reload <cogs_name>",
    )
    @commands.guild_only()
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


def setup(bot):
    bot.add_cog(System(bot))
