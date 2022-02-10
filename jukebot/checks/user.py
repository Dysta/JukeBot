from nextcord.ext.commands import Context, CheckFailure

from jukebot.components import Player


def is_dysta(ctx: Context):
    if not ctx.message.author.id == 845189167914549288:
        raise CheckFailure("You're not Dysta.")
    return True


def bot_queue_is_not_empty(ctx: Context):
    player: Player = ctx.bot.players[ctx.guild.id]
    if player.queue.is_empty():
        raise CheckFailure("The queue is empty.")
    return True


def guild_is_blacklist(ctx: Context):
    if ctx.bot.is_blacklist(ctx.guild.id):
        raise CheckFailure("Your guild is banned.")
    return True
