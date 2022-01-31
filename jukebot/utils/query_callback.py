from loguru import logger
from nextcord import Message

from nextcord.ext.commands import Context

from jukebot.utils import embed


async def failure(ctx: Context, query: str, full_query: str):
    logger.opt(lazy=True).debug(
        f"Query '{query}' ({full_query}) failed for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
    )
    e = embed.music_not_found_message(
        ctx.author,
        title="Query failed..",
        content=f"Nothing found for `{query}`.",
    )
    await ctx.send(embed=e, delete_after=5.0)


async def cancel(ctx: Context, msg: Message, query: str, full_query: str):
    logger.opt(lazy=True).debug(
        f"Query '{query}' ({full_query}) canceled for guild '{ctx.guild.name} (ID: {ctx.guild.id})'."
    )
    e = embed.music_not_found_message(
        ctx.author,
        title=f"Search canceled",
    )
    await msg.edit(embed=e, delete_after=5.0)
