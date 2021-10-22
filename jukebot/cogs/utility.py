import typing
from datetime import datetime

from embed import Embed
import discord
from discord.ext import commands


class Utiliy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["h"])
    @commands.guild_only()
    async def help_message(self, ctx):
        e = Embed.error_message(ctx, title="Help msg")
        await ctx.send(embed=e)

    @commands.command(aliases=["i"])
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

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        e = Embed.info_message(ctx, content=f"Pong.. {self.bot.latency * 1000:.2f}ms")
        await ctx.reply(embed=e)

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
    async def echo(self, ctx, *, args):
        await ctx.send(args)

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, who: typing.Optional[discord.Member] = None):
        e = Embed.basic_message(
            ctx, title=f"{ctx.author if who is None else who}'s avatar"
        )
        e.set_image(url=ctx.author.avatar_url if who is None else who.avatar_url)
        await ctx.send(embed=e)
