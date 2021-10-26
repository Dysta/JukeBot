import typing
from datetime import datetime

from embed import Embed
import discord
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["i"],
        brief="Get info about the bot",
        help="Get information about the bot like the ping and the uptime.",
        usage="info",
    )
    @commands.guild_only()
    async def info(self, ctx):
        e = Embed.info_message(ctx)
        e.add_field(name="Ping", value=f"{self.bot.latency * 1000:.2f}ms", inline=False)
        uptime = datetime.now() - self.bot.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        e.add_field(
            name="Uptime",
            value=f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds",
            inline=False,
        )
        await ctx.reply(embed=e)

    @commands.command(
        brief="Check the bot latency",
        help="Return the current latency of the bot.",
        usage="ping",
    )
    @commands.guild_only()
    async def ping(self, ctx):
        e = Embed.info_message(ctx, content=f"Pong.. {self.bot.latency * 1000:.2f}ms")
        await ctx.reply(embed=e)

    @commands.command(hidden=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member):
        try:
            await member.kick(reason=None)
            await ctx.send(
                "kicked " + member.mention
            )  # simple kick command to demonstrate how to get and use member mentions
        except:
            await ctx.send("bot does not have the kick members permission!")

    @commands.command(
        brief="Repeat a message", help="Repeat message", usage="echo <message>"
    )
    @commands.guild_only()
    async def echo(self, ctx, *, args):
        await ctx.send(args)

    @commands.command(
        brief="Display a user avatar",
        help="Display a user avatar in a embed message.\nIf no user is provided, it will show the command invoker avatar.",
        usage="avatar [member]",
    )
    @commands.guild_only()
    async def avatar(self, ctx, who: typing.Optional[discord.Member] = None):
        who = ctx.author if who is None else who
        e = Embed.basic_message(ctx, title=f"{who}'s avatar")
        e.set_image(url=who.avatar_url)
        await ctx.send(embed=e)
