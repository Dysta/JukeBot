import os
import typing

from datetime import datetime

from loguru import logger
from nextcord import AllowedMentions, InviteTarget, Member, Permissions, Embed
from nextcord.ext import commands
from nextcord.ext.commands import Context, BucketType, Bot

from jukebot.checks import voice
from jukebot.components import Player
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
    @commands.cooldown(1, 10.0, BucketType.user)
    @commands.guild_only()
    async def info(self, ctx: Context):
        e = embed.info_message(ctx.author)
        e.add_field(
            name="🤖 Name", value=f"┕`{self.bot.user.display_name}`", inline=True
        )
        e.add_field(
            name="📡 Ping", value=f"┕`{self.bot.latency * 1000:.2f}ms`", inline=True
        )
        uptime = datetime.now() - self.bot.start_time
        days, hours, minutes, seconds = converter.seconds_to_time(
            int(uptime.total_seconds())
        )
        e.add_field(
            name="⏱ Uptime",
            value=f"┕`{days}d, {hours}h, {minutes}m, {seconds}s`",
            inline=True,
        )
        e.add_field(name="🏛️ Servers", value=f"┕`{self.bot.guilds_count}`", inline=True)
        e.add_field(
            name="👥 Members",
            value=f"┕`{self.bot.members_count}`",
            inline=True,
        )
        e.add_field(
            name="🪄 Prefix",
            value=f"┕`{await self.bot.prefixes.get_item(ctx.guild.id)}`",
            inline=True,
        )
        e.set_image(
            url="https://cdn.discordapp.com/attachments/829356508696412231/948936347752747038/juke-banner.png"
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

    @commands.command(
        aliases=["pfx"],
        brief="Change/Display the prefix of the bot",
        help="Set a new prefix for the bot.\nIf no prefix are given, sends the current server prefix.",
        usage="[prefix]",
    )
    @commands.guild_only()
    @commands.cooldown(1, 15.0, BucketType.guild)
    async def prefix(self, ctx: Context, prefix: typing.Optional[str] = None):
        if not prefix:
            e = embed.basic_message(
                ctx.author,
                content=f"Prefix for `{ctx.guild.name}` is `{await self.bot.prefixes.get_item(ctx.guild.id)}`",
            )
            await ctx.send(embed=e)
            return

        perm: Permissions = ctx.author.guild_permissions
        logger.opt(lazy=True).info(
            f"Set prefix '{prefix}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
        )
        if perm.administrator:
            await self.bot.prefixes.set_item(ctx.guild.id, prefix)
            e = embed.basic_message(
                ctx.author,
                title="Prefix changed!",
                content=f"Prefix is set to `{prefix}` for server `{ctx.guild.name}`",
            )
            logger.opt(lazy=True).success(
                f"Successfully set prefix '{prefix}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
            )
        else:
            e = embed.error_message(
                ctx.author, content="You're not administrator of this server."
            )
            logger.opt(lazy=True).error(
                f"Missing permission for setting prefix '{prefix}' for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
            )
        await ctx.send(embed=e)

    @commands.command(
        aliases=["rst"],
        brief="Force reset the current player",
        help="Reset the current guild player when something is wrong.\nUse it when the bot can't connect to voice channel even if everything is ok.",
    )
    @commands.guild_only()
    @commands.cooldown(1, 15.0, BucketType.guild)
    async def reset(self, ctx: Context):
        if not ctx.guild.id in self.bot.players:
            logger.opt(lazy=True).debug(
                f"Server {ctx.guild.name} ({ctx.guild.id}) try to kill a player that don't exist."
            )
            e: Embed = embed.error_message(
                ctx.author, content="No player detected in this server."
            )
            await ctx.send(embed=e)
            return

        player: Player = self.bot.players.pop(ctx.guild.id)
        try:
            await player.disconnect(force=True)
        except Exception as e:
            logger.opt(lazy=True).error(
                f"Error when force disconnecting the player of the guild {ctx.guild.name} ({ctx.guild.id}). "
                f"Error: {e}"
            )

        logger.opt(lazy=True).success(
            f"Server {ctx.guild.name} ({ctx.guild.id}) has successfully reset his player."
        )
        e: Embed = embed.info_message(ctx.author, content="The player has been reset.")
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Utility(bot))
    bot.help_command.cog = bot.get_cog("Utility")
