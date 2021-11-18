import discord
import typing

from datetime import datetime

from discord.ext import commands
from discord.ext.commands import Context

from jukebot.utils import embed, converter


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["i"],
        brief="Get info about the bot",
        help="Get information about the bot like the ping and the uptime.",
    )
    @commands.guild_only()
    async def info(self, ctx: Context):
        e = embed.info_message(ctx)
        e.add_field(name="Ping", value=f"{self.bot.latency * 1000:.2f}ms", inline=False)
        uptime = datetime.now() - self.bot.start_time
        days, hours, minutes, seconds = converter.seconds_to_time(
            int(uptime.total_seconds())
        )
        e.add_field(
            name="Uptime",
            value=f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds",
            inline=False,
        )
        await ctx.reply(embed=e)

    @commands.command(
        brief="Check the bot latency",
        help="Return the current latency of the bot.",
    )
    @commands.guild_only()
    async def ping(self, ctx: Context):
        e = embed.info_message(ctx, content=f"Pong.. {self.bot.latency * 1000:.2f}ms")
        await ctx.reply(embed=e)

    @commands.command(
        aliases=["say"],
        brief="Repeat a message",
        help="Repeat message",
        usage="<message>",
    )
    @commands.guild_only()
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args)

    @commands.command(
        brief="Display a user avatar",
        help="Display a user avatar in a embed message.\nIf no user is provided, it will show the command invoker avatar.",
        usage="[member]",
    )
    @commands.guild_only()
    async def avatar(self, ctx: Context, who: typing.Optional[discord.Member] = None):
        who = ctx.author if who is None else who
        e = embed.basic_message(ctx, title=f"{who}'s avatar")
        e.set_image(url=who.avatar_url)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Utility(bot))
    bot.help_command.cog = bot.get_cog("Utility")
