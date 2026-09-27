from __future__ import annotations

import io
import os
from datetime import datetime
from typing import TYPE_CHECKING

from disnake import CommandInteraction, File
from disnake.ext import commands
from loguru import logger

from jukebot.utils import Extensions, converter
from jukebot.views.embed import VOID_TOKEN, info_message

if TYPE_CHECKING:
    from jukebot import JukeBot

ADMIN_GUILD_IDS = (
    list(map(int, os.environ["BOT_ADMIN_GUILD_IDS"].split(","))) if "BOT_ADMIN_GUILD_IDS" in os.environ else []
)


class System(commands.Cog):
    def __init__(self, bot):
        self.bot: JukeBot = bot

    def _reload_all_cogs(self):
        logger.opt(lazy=True).info("Reloading all extensions.")
        for e in Extensions.all():
            self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
            logger.opt(lazy=True).success(f"Extension {e['package']}.{e['name']} reloaded.")
        logger.opt(lazy=True).info("All extensions have been successfully reloaded.")

    def _reload_cog(self, name):
        logger.opt(lazy=True).info(f"Reloading '{name}' extension.")
        e = Extensions.get(name)
        if e is None:
            logger.error(f"Extension {name!r} could not be loaded.")
            raise commands.ExtensionNotFound(name)
        self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
        logger.opt(lazy=True).success(f"Extension {e['package']}.{e['name']} reloaded.")

    @commands.slash_command(
        guild_ids=ADMIN_GUILD_IDS,
    )
    @commands.is_owner()
    async def reload(self, inter: CommandInteraction, cog_name: str | None = None):
        """Reload the given cog. If no cog is given, reload all cogs.

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        cog_name : Optional[str], optional
            The cog name to reload, by default None
        """
        try:
            if not cog_name:
                self._reload_all_cogs()
            else:
                self._reload_cog(cog_name)
        except Exception as e:
            await inter.send(f"❌ | {e}", ephemeral=True)
            return

        await inter.send("✅ | reloaded", ephemeral=True)

    @commands.slash_command(guild_ids=ADMIN_GUILD_IDS)
    @commands.is_owner()
    async def refresh(self, inter: CommandInteraction):
        """Updates all cached properties of the bot

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        try:
            del self.bot.members_count
            logger.opt(lazy=True).success("Members count reset.")
            del self.bot.guilds_count
            logger.opt(lazy=True).success("Guilds count reset.")
        except Exception as e:
            await inter.send(f"❌ | {e}", ephemeral=True)
            return

        await inter.send("✅ | refresh", ephemeral=True)

    @commands.slash_command(guild_ids=ADMIN_GUILD_IDS)
    @commands.is_owner()
    async def stats(self, inter: CommandInteraction):
        """Displays bot statistics such as number of servers, users or players created

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        e = info_message(title=f"Stats about {self.bot.user.name}")
        e.add_field(name="📡 Ping", value=f"┕`{self.bot.latency * 1000:.2f}ms`")
        uptime = datetime.now() - self.bot.start_time
        days, hours, minutes, seconds = converter.seconds_to_time(int(uptime.total_seconds()))
        e.add_field(
            name="⏱ Uptime",
            value=f"┕`{days}d, {hours}h, {minutes}m, {seconds}s`",
        )
        e.add_field(name=VOID_TOKEN, value=VOID_TOKEN)
        e.add_field(name="🏛️ Servers", value=f"┕`{len(self.bot.guilds)}`", inline=True)
        e.add_field(
            name="👥 Members",
            value=f"┕`{len(set(self.bot.get_all_members()))}`",
        )
        e.add_field(name=VOID_TOKEN, value=VOID_TOKEN)
        e.add_field(
            name="📻 Players created",
            value=f"┕`{len(self.bot.players)}`",
        )
        e.add_field(
            name="🎶 Players playing",
            value=f"┕`{len(self.bot.players.playing())}`",
        )
        e.add_field(name=VOID_TOKEN, value=VOID_TOKEN)

        await inter.send(embed=e, ephemeral=True)

    @commands.slash_command(guild_ids=ADMIN_GUILD_IDS)
    @commands.is_owner()
    async def commands(self, inter: CommandInteraction):
        """Generates a .yaml file containing all bot commands

        Parameters
        ----------
        inter : CommandInteraction
            The interaction
        """
        cmds = sorted(self.bot.slash_commands, key=lambda x: x.name)
        msg: str = "---\n"
        for c in cmds:
            opts: str = ""
            if c.body.options:
                opts = " ".join([e.name for e in c.body.options])
            msg += f"""
- title: {c.name}
  icon: none
  usage: /{c.name} {opts}
  desc: {c.body.description}
"""
        data = io.BytesIO(msg.encode())
        await inter.send(file=File(data, "cmds.yaml"), ephemeral=True)


def setup(bot: JukeBot):
    bot.add_cog(System(bot))
