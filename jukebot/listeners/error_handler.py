from discord.ext import commands
from jukebot.utils import embed


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"{error=}")
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("⁉")
            return

        e = embed.error_message(ctx, content=error)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
