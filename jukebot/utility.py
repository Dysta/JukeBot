from embed import Embed
import discord
from discord.ext import commands


class Utiliy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["h"])
    @commands.guild_only()
    async def help_message(self, ctx):
        e = Embed.error_message(title="Help msg")
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        await ctx.send(
            "pong!"
        )  # simple command so that when you type "!ping" the bot will respond with "pong!"

    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member):
        try:
            await member.kick(reason=None)
            await ctx.send(
                "kicked " + member.mention
            )  # simple kick command to demonstrate how to get and use member mentions
        except:
            await ctx.send("bot does not have the kick members permission!")

    @commands.command()
    @commands.guild_only()
    async def echo(self, ctx, *args):
        await ctx.send(" ".join(args))

    # async def cog_command_error(self, ctx, exception):
    #     print(f"{exception=}")
    #     e = Embed.error_message(content=exception, footer=f"Try {ctx.prefix}help")
    #     await ctx.send(embed=e)
