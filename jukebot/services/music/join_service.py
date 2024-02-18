from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional


from jukebot.abstract_components import AbstractService
from jukebot.exceptions import PlayerConnexionException
from jukebot.utils import embed

if TYPE_CHECKING:
    from jukebot.components import Player


class JoinService(AbstractService):
    async def __call__(
        self,
        /,
        silent: Optional[bool] = False,
    ):
        player: Player = self.bot.players[self.interaction.guild.id]
        try:
            await player.join(self.interaction.author.voice.channel)
        except:
            # we remove the created player
            self.bot.players.pop(self.interaction.guild.id)
            raise PlayerConnexionException(
                f"Can't connect to **{self.interaction.author.voice.channel.name}**. "
                f"Check both __bot__ and __channel__ permissions."
            )

        if not silent:
            e = embed.basic_message(
                content=f"Connected to <#{self.interaction.author.voice.channel.id}>\n"
                f"Bound to <#{self.interaction.channel.id}>\n",
            )
            await self.interaction.send(embed=e)

        cpy_inter = copy.copy(self.interaction)
        # time to trick the copied interaction
        # used to display bot as invoker
        cpy_inter.author = self.bot.user
        # used to send a message in the channel instead of replying to an interaction
        # NB: possible source of bug, edit_original_message take content as a kwargs compare to send
        cpy_inter.send = cpy_inter.edit_original_message = cpy_inter.channel.send

        player.interaction = cpy_inter
        return True
