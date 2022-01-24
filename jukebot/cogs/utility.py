import os
import typing

from datetime import datetime

from nextcord import AllowedMentions, InviteTarget, Member
from nextcord.ext import commands
from nextcord.ext.commands import Context, BucketType, Bot

from jukebot.checks import voice
from jukebot.utils import embed, converter, applications
from jukebot.views import ActivityView


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
        e.add_field(name="🏛️ Servers", value=f"`{self.bot.guilds_count}`", inline=True)
        e.add_field(
            name="👨‍👧‍👦 Members",
            value=f"`{self.bot.members_count}`",
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
        await ctx.send(args, allowed_mentions=AllowedMentions.none())

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

    @commands.command(
        brief="Send the invite link",
        help="Send the invite link.",
    )
    @commands.cooldown(1, 8.0, BucketType.user)
    @commands.guild_only()
    async def invite(self, ctx: Context):
        msg: str = (
            f"To invite `{self.bot.user.name}`, click on this link: "
            f"{os.environ['BOT_INVITE_URL']}\n"
            f"Thanks for support :heart:"
        )
        await ctx.send(content=msg)

    @commands.command(
        brief="Send the vote link",
        help="Send the vote link.",
    )
    @commands.cooldown(1, 8.0, BucketType.user)
    @commands.guild_only()
    async def vote(self, ctx: Context):
        msg: str = (
            f"To vote for `{self.bot.user.name}`, click on this link: "
            f"{os.environ['BOT_VOTE_URL']}\n"
            f"Thanks for support :heart:"
        )
        await ctx.send(content=msg)

    @commands.command(
        brief="Send the donate link",
        help="Send the donate link.",
    )
    @commands.cooldown(1, 8.0, BucketType.user)
    @commands.guild_only()
    async def donate(self, ctx: Context):
        msg: str = (
            f"To financially support `{self.bot.user.name}`, click on this link: "
            f"{os.environ['BOT_DONATE_URL']}\n"
            f"Thanks for support :heart:"
        )
        await ctx.send(content=msg)

    @commands.command(hidden=True)
    @commands.guild_only()
    async def zizi(self, ctx: Context):
        await ctx.reply("caca")

    @commands.command(
        aliases=["w"],
        brief="Launch a Youtube Together session",
        help="Launch a Youtube Together session in the current voice channel the invoker is.",
    )
    @commands.cooldown(1, 15.0, BucketType.guild)
    @commands.max_concurrency(1, BucketType.guild)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def watch(self, ctx: Context):
        max_time = 180
        invite = await ctx.author.voice.channel.create_invite(
            max_age=max_time,
            reason="Watch Together",
            target_type=InviteTarget.embedded_application,
            target_application_id=applications.default["youtube"],
        )
        e = embed.activity_message(
            ctx.author,
            "Watch Together started!",
            f"An activity started in `{ctx.author.voice.channel.name}`.\n",
        )

        await ctx.reply(
            embed=e, view=ActivityView(invite.url), delete_after=float(max_time)
        )


def setup(bot):
    bot.add_cog(Utility(bot))
    bot.help_command.cog = bot.get_cog("Utility")
