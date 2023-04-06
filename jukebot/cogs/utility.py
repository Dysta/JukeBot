from __future__ import annotations

from datetime import datetime
from typing import Optional

from disnake import CommandInteraction, InviteTarget, Member
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from jukebot.services import ResetService
from jukebot.utils import applications, checks, converter, embed
from jukebot.views import ActivityView, PromoteView


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command(
        description="Get information about the bot like the ping and the uptime.",
    )
    @commands.cooldown(1, 10.0, BucketType.user)
    async def info(self, inter: CommandInteraction):
        e = embed.info_message(inter.author)
        e.add_field(name="🤖 Name", value=f"┕`{self.bot.user.display_name}`", inline=True)
        e.add_field(name="📡 Ping", value=f"┕`{self.bot.latency * 1000:.2f}ms`", inline=True)
        uptime = datetime.now() - self.bot.start_time
        days, hours, minutes, seconds = converter.seconds_to_time(int(uptime.total_seconds()))
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
            value=f"┕`/`",
            inline=True,
        )
        e.set_image(
            url="https://cdn.discordapp.com/attachments/829356508696412231/948936347752747038/juke-banner.png"
        )
        await inter.send(embed=e, ephemeral=True)

    @commands.slash_command(
        description="Display a user avatar in a embed message. If no user, it will show the command invoker avatar.",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    async def avatar(self, inter: CommandInteraction, user: Optional[Member] = None):
        user: Member = inter.author if user is None else user
        e = embed.basic_message(inter.author, title=f"{user.name}'s avatar")
        e.set_image(url=user.display_avatar.url)
        await inter.send(embed=e)

    @commands.slash_command(description="Send all links to support the bot")
    @commands.cooldown(1, 8.0, BucketType.user)
    async def links(self, inter: CommandInteraction):
        await inter.send(view=PromoteView())

    @commands.slash_command(
        description="Launch a Youtube Together session in the current voice channel the invoker is.",
    )
    @commands.cooldown(1, 15.0, BucketType.guild)
    @commands.max_concurrency(1, BucketType.guild)
    @commands.check(checks.user_is_connected)
    async def watch(self, inter: CommandInteraction):
        max_time = 180
        invite = await inter.author.voice.channel.create_invite(
            max_age=max_time,
            reason="Watch Together",
            target_type=InviteTarget.embedded_application,
            target_application=applications.default["youtube"],
        )
        e = embed.activity_message(
            inter.author,
            "Watch Together started!",
            f"An activity started in `{inter.author.voice.channel.name}`.\n",
        )

        await inter.send(embed=e, view=ActivityView(invite.url), delete_after=float(max_time))

    @commands.slash_command(
        description="Reset the current guild player when something is wrong.",
    )
    @commands.cooldown(1, 15.0, BucketType.guild)
    async def reset(self, inter: CommandInteraction):
        with ResetService(self.bot) as rs:
            await rs(interaction=inter)


def setup(bot):
    bot.add_cog(Utility(bot))
