from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import CommandInteraction
from disnake.ext.commands import CheckFailure

if TYPE_CHECKING:
    from jukebot.components import Player


def bot_queue_is_not_empty(inter: CommandInteraction):
    player: Player = inter.bot.players[inter.guild.id]
    if player.queue.is_empty():
        raise CheckFailure("The queue is empty.")
    return True
