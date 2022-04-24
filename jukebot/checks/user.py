from disnake.ext.commands import Context, CheckFailure

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
