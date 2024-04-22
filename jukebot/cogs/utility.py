from __future__ import annotations

from datetime import datetime

from disnake import CommandInteraction, InviteTarget
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
        """Displays information about the bot like its ping, uptime, prefix and more

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        e = embed.info_message()
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
        e.set_image(url="https://cdn.discordapp.com/attachments/829356508696412231/948936347752747038/juke-banner.png")
        await inter.send(embed=e, ephemeral=True)

    @commands.slash_command()
    @commands.cooldown(1, 8.0, BucketType.user)
    async def links(self, inter: CommandInteraction):
        """Send all links to support the bot

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        await inter.send(view=PromoteView())

    @commands.slash_command()
    @commands.cooldown(1, 15.0, BucketType.guild)
    @commands.max_concurrency(1, BucketType.guild)
    @commands.check(checks.user_is_connected)
    async def watch(self, inter: CommandInteraction):
        """Launch a Youtube Together session in the voice channel where you are currently.

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        max_time = 180
        invite = await inter.author.voice.channel.create_invite(
            max_age=max_time,
            reason="Watch Together",
            target_type=InviteTarget.embedded_application,
            target_application=applications.default["youtube"],
        )
        e = embed.activity_message(
            "Watch Together started!",
            f"An activity started in `{inter.author.voice.channel.name}`.\n",
        )

        await inter.send(embed=e, view=ActivityView(invite.url), delete_after=float(max_time))

    @commands.slash_command()
    @commands.cooldown(1, 15.0, BucketType.guild)
    async def reset(self, inter: CommandInteraction):
        """Disconnects the bot and resets its internal state if something isn't working.

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        with ResetService(self.bot) as rs:
            await rs(interaction=inter)


def setup(bot):
    bot.add_cog(Utility(bot))
