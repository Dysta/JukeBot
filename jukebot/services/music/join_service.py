from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from disnake import CommandInteraction

from jukebot.abstract_components import AbstractService
from jukebot.exceptions import PlayerConnexionException

if TYPE_CHECKING:
    from jukebot.components import Player


class JoinService(AbstractService):
    async def __call__(
        self,
        /,
        interaction: CommandInteraction,
    ):
        player: Player = self.bot.players[interaction.guild.id]
        try:
            await player.join(interaction.author.voice.channel)
        except:
            # we remove the created player
            self.bot.players.pop(interaction.guild.id)

            cmd = self.bot.get_global_command_named("reset")
            raise PlayerConnexionException(
                f"Can't connect to **{interaction.author.voice.channel.name}**. "
                f"Check both __bot__ and __channel__ permissions.\n"
                f"If the issue persists, try to reset your player with </reset:{cmd.id}>."
            )

        cpy_inter = copy.copy(interaction)
        # time to trick the copied interaction
        # used to display bot as invoker
        cpy_inter.author = self.bot.user
        # used to send a message in the channel instead of replying to an interaction
        # NB: possible source of bug, edit_original_message take content as a kwargs compare to send
        cpy_inter.send = cpy_inter.edit_original_message = cpy_inter.channel.send

        player.interaction = cpy_inter
