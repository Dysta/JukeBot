from datetime import datetime
from typing import Optional

from loguru import logger

from disnake.ext import commands
from disnake.ext.commands import Context

from jukebot.utils import Extensions, embed, converter


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _reload_all_cogs(self):
        logger.opt(lazy=True).info("Reloading all extensions.")
        for e in Extensions.all():
            self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
            logger.opt(lazy=True).success(
                f"Extension {e['package']}.{e['name']} reloaded."
            )
        logger.opt(lazy=True).info("All extensions have been successfully reloaded.")

    def _reload_cog(self, name):
        logger.opt(lazy=True).info(f"Reloading '{name}' extension.")
        e = Extensions.get(name)
        if e is None:
            logger.error(f"Extension {name!r} could not be loaded.")
            raise commands.ExtensionNotFound(name)
        self.bot.reload_extension(name=f"{e['package']}.{e['name']}")
        logger.opt(lazy=True).success(f"Extension {e['package']}.{e['name']} reloaded.")

    @commands.command(
        aliases=["rld"],
        brief="Reload a cog or all cogs",
        help="Reload the given cog. If no cog is given, reload all cogs.",
        usage="reload [cogs_name]",
        hidden=True,
    )
    @commands.guild_only()
    @commands.is_owner()
    async def reload(self, ctx, cog_name: Optional[str] = None):
        try:
            if not cog_name:
                self._reload_all_cogs()
            else:
                self._reload_cog(cog_name)
        except Exception:
            await ctx.message.add_reaction("❌")
            raise
        await ctx.message.add_reaction("✅")

    @commands.command(
        aliases=["rfsh"],
        brief="Reset all cached property.",
        help="Reset all cached property of the bot.",
        hidden=True,
    )
    @commands.guild_only()
    @commands.is_owner()
    async def refresh(self, ctx: Context):
        try:
            del self.bot.members_count
            logger.opt(lazy=True).success("Members count reset.")
            del self.bot.guilds_count
            logger.opt(lazy=True).success("Guilds count reset.")
        except Exception:
            await ctx.message.add_reaction("❌")
            raise
        await ctx.message.add_reaction("✅")

    @commands.command(
        brief="Share stats about the bot.",
        help="Share stats about the bot.",
        hidden=True,
    )
    @commands.guild_only()
    @commands.is_owner()
    async def stats(self, ctx: Context):
        e = embed.info_message(ctx.author, title=f"Stats about {self.bot.user.name}")
        e.add_field(name="📡 Ping", value=f"┕`{self.bot.latency * 1000:.2f}ms`")
        uptime = datetime.now() - self.bot.start_time
        days, hours, minutes, seconds = converter.seconds_to_time(
            int(uptime.total_seconds())
        )
        e.add_field(
            name="⏱ Uptime",
            value=f"┕`{days}d, {hours}h, {minutes}m, {seconds}s`",
        )
        e.add_field(name=embed.VOID_TOKEN, value=embed.VOID_TOKEN)
        e.add_field(name="🏛️ Servers", value=f"┕`{len(self.bot.guilds)}`", inline=True)
        e.add_field(
            name="👥 Members",
            value=f"┕`{len(set(self.bot.get_all_members()))}`",
        )
        e.add_field(name=embed.VOID_TOKEN, value=embed.VOID_TOKEN)
        e.add_field(
            name="📻 Players created",
            value=f"┕`{len(self.bot.players)}`",
        )
        e.add_field(
            name="🎶 Players playing",
            value=f"┕`{len(self.bot.players.playing())}`",
        )
        e.add_field(name=embed.VOID_TOKEN, value=embed.VOID_TOKEN)

        await ctx.reply(embed=e, mention_author=False)


def setup(bot):
    bot.add_cog(System(bot))
