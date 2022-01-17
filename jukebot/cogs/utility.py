import typing

from datetime import datetime

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context, BucketType, Bot
from nextcord import Member

from jukebot.utils import embed, converter


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.command(
        aliases=["i"],
        brief="Get info about the bot",
        help="Get information about the bot like the ping and the uptime.",
    )
    @commands.cooldown(1, 15.0, BucketType.user)
    @commands.guild_only()
    async def info(self, ctx: Context):
        e = embed.info_message(ctx.author)
        e.set_thumbnail(url=self.bot.user.display_avatar.url)
        e.add_field(name="🤖 Name", value=f"`{self.bot.user.display_name}`", inline=True)
        e.add_field(
            name="📍 Ping", value=f"`{self.bot.latency * 1000:.2f}ms`", inline=True
        )
        uptime = datetime.now() - self.bot.start_time
        days, hours, minutes, seconds = converter.seconds_to_time(
            int(uptime.total_seconds())
        )
        e.add_field(
            name="📊 Uptime",
            value=f"`{days}d, {hours}h, {minutes}m, {seconds}s`",
            inline=True,
        )
        e.add_field(
            name="🏛️ Servers", value=f"`{str(len(self.bot.guilds))}`", inline=True
        )
        e.add_field(
            name="👨‍👧‍👦 Members",
            value=f"`{len(set(self.bot.get_all_members()))}`",
            inline=True,
        )
        e.add_field(
            name="🪄 Prefix",
            value=f"`{await self.bot.prefixes.get_item(ctx.guild.id)}`",
            inline=True,
        )
        await ctx.reply(embed=e)

    @commands.command(
        brief="Check the bot latency",
        help="Return the current latency of the bot.",
    )
    @commands.cooldown(1, 15.0, BucketType.user)
    @commands.guild_only()
    async def ping(self, ctx: Context):
        e = embed.info_message(
            ctx.author, content=f"Pong.. {self.bot.latency * 1000:.2f}ms"
        )
        await ctx.reply(embed=e)

    @commands.command(
        aliases=["say"],
        brief="Repeat a message",
        help="Repeat message",
        usage="<message>",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args, allowed_mentions=nextcord.AllowedMentions.none())

    @commands.command(
        brief="Display a user avatar",
        help="Display a user avatar in a embed message.\nIf no user is provided, it will show the command invoker avatar.",
        usage="[member]",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx: Context, who: typing.Optional[Member] = None):
        who: Member = ctx.author if who is None else who
        e = embed.basic_message(ctx.author, title=f"{who}'s avatar")
        e.set_image(url=who.display_avatar.url)
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    @commands.guild_only()
    async def zizi(self, ctx: Context):
        await ctx.reply("caca")


def setup(bot):
    bot.add_cog(Utility(bot))
    bot.help_command.cog = bot.get_cog("Utility")
