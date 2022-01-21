from loguru import logger

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