import discord
from discord.ext import commands
from embed import Embed


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"{error=}")
        await ctx.message.add_reaction("⁉")
        return
        # if isinstance(error, commands.CommandNotFound):
        #     # TODO: finish error handling
        #     pass
        #
        # e = Embed.error_message(ctx, content=error)
def setup(bot):
    bot.add_cog(ErrorHandler(bot))
