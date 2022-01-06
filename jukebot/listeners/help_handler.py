import itertools

from nextcord.ext import commands

from jukebot.utils import embed


class HelpHandler(commands.HelpCommand):
    def __init__(self):
        opts = {
            "aliases": ["h"],
            "brief": "Show the help message",
            "help": "Display a list of all available commands.\nCan display help for a specific category or command.",
            "usage": "[command_name|category_name]",
        }
        super().__init__(verify_checks=False, command_attrs=opts)

    def get_ending_note(self):
        command_name = self.invoked_with
        return (
            f"Type `{self.context.prefix}{command_name} command` for more info on a command.",
            f"Type `{self.context.prefix}{command_name} category` for more info on a category.",
        )

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot

        help_embed = embed.info_message(ctx.author, title="Available commands")

        def get_category(command, *, no_category="Other:"):
            cog = command.cog
            return cog.qualified_name if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)

        for category, cmds in to_iterate:
            cmds = sorted(cmds, key=lambda c: c.name)
            cmds_str = ", ".join([f"{c.name}" for c in cmds])
            help_embed.add_field(name=category, value=f"```{cmds_str}```", inline=False)

        note = self.get_ending_note()
        if note:
            help_embed.add_field(
                name=embed.VOID_TOKEN, value="\n".join(note), inline=False
            )

        await ctx.send(embed=help_embed)

    async def send_cog_help(self, cog):
        ctx = self.context

        cog_embed = embed.info_message(ctx.author, title="Available commands")

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        cmds = sorted(filtered, key=lambda c: c.name)
        cmds_str = "\n".join([f"{c.name} - {c.short_doc}" for c in cmds])

        cog_embed.add_field(
            name=cog.qualified_name, value=f"```{cmds_str}```", inline=False
        )
        note = self.get_ending_note()
        if note:
            cog_embed.add_field(name=embed.VOID_TOKEN, value=note[0], inline=False)

        await ctx.send(embed=cog_embed)

    async def send_command_help(self, command):
        ctx = self.context

        cmd_str = (
            f"{command.full_parent_name } {command.name}"
            if command.parent
            else command.name
        )
        cmd_embed = embed.info_message(
            ctx.author, title=f"Command : {cmd_str}", content=command.help
        )

        aliases = ", ".join([a for a in [command.name] + command.aliases])
        cmd_embed.add_field(name="Aliases", value=f"```{aliases}```", inline=False)

        if not command.parent:
            cmd_embed.add_field(
                name="Usage",
                value=f"```{ctx.prefix}{command.name} {command.usage if command.usage is not None else ''}```",
                inline=False,
            )
        else:
            cmd_embed.add_field(
                name="Usage",
                value=f"```{ctx.prefix}{command.full_parent_name} {command.name} {command.usage if command.usage is not None else ''}```",
                inline=False,
            )

        await ctx.send(embed=cmd_embed)

    async def send_group_help(self, group):
        ctx = self.context

        grp_embed = embed.info_message(
            ctx.author, title=f"Command : {group.name}", content=group.help
        )

        aliases = ", ".join([a for a in [group.name] + group.aliases])
        grp_embed.add_field(name="Aliases", value=f"```{aliases}```", inline=False)

        subcmds = ", ".join(
            [c.name for c in sorted(group.commands, key=lambda c: c.name)]
        )
        grp_embed.add_field(
            name="Subcommands",
            value=f"```{subcmds}```",
            inline=False,
        )

        usg_subcmds = subcmds.replace(", ", "|")
        grp_embed.add_field(
            name="Usage",
            value=f"```{ctx.prefix}{group.name} <{usg_subcmds}>```",
            inline=False,
        )

        note = self.get_ending_note()
        grp_embed.add_field(name=embed.VOID_TOKEN, value=note[0], inline=False)

        await ctx.send(embed=grp_embed)
