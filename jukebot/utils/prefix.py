import os

from loguru import logger
from nextcord.ext import commands


async def _prefix_for(client, message):
    prefixes = client.prefixes
    guild_id = message.guild.id
    if (prefix := await prefixes.get_item(guild_id)) is None:
        await prefixes.set_item(guild_id, os.environ["BOT_PREFIX"])
        prefix = os.environ["BOT_PREFIX"]

    logger.opt(lazy=True).debug(
        f"Return prefix '{prefix}' for guild {message.guild} (ID: {guild_id})"
    )
    return prefix


async def get_prefix(client, message):
    prefix = await _prefix_for(client, message)
    return commands.when_mentioned_or(prefix)(client, message)
