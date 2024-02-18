from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import Member, VoiceChannel, VoiceState
from disnake.ext import commands
from disnake.ext.commands import Bot

from jukebot.services.music import PauseService, ResumeService

if TYPE_CHECKING:
    from jukebot.components import Player


class VoiceHandler(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel != after.channel:
            if before.channel is None:
                self.bot.dispatch("voice_channel_connect", member, after.channel)
            elif after.channel is None:
                self.bot.dispatch("voice_channel_disconnect", member, before.channel)
                if len(before.channel.members) == 1:
                    self.bot.dispatch("voice_channel_alone", member, before.channel)
            else:
                self.bot.dispatch("voice_channel_move", member, before.channel, after.channel)

    @commands.Cog.listener()
    async def on_voice_channel_connect(self, member: Member, channel: VoiceChannel):
        if member == self.bot.user:
            return
        if self.bot.user in channel.members:
            player: Player = self.bot.players[channel.guild.id]
            if player.is_paused:
                with ResumeService(self.bot, player.interaction) as resume:
                    await resume(silent=True)

    @commands.Cog.listener()
    async def on_voice_channel_alone(self, member: Member, channel: VoiceChannel):
        if channel.members[0].id == self.bot.user.id:
            player: Player = self.bot.players[channel.guild.id]
            if player.is_playing:
                with PauseService(self.bot, player.interaction) as pause:
                    await pause(silent=True)


def setup(bot):
    bot.add_cog(VoiceHandler(bot))
