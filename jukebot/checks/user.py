from nextcord import Embed
from nextcord.ext.commands import Context

from jukebot.utils import embed


class UserChecks:
    @staticmethod
    async def is_dysta(ctx: Context):
        if not ctx.message.author.id == 845189167914549288:
            e: Embed = embed.error_message(
                ctx, content="You're not the bot owner."
            )
            await ctx.send(embed=e)
            return False
        return True
