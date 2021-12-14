from nextcord import Member, VoiceState, VoiceChannel
from nextcord.ext import commands
from nextcord.ext.commands import Bot

from jukebot.components import Player


class VoiceHandler(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if before.channel != after.channel:
            if before.channel is None:
                self.bot.dispatch("voice_channel_connect", member, after.channel)
            elif after.channel is None:
                self.bot.dispatch("voice_channel_disconnect", member, before.channel)
                if len(before.channel.members) == 1:
                    self.bot.dispatch("voice_channel_alone", member, before.channel)
            else:
                self.bot.dispatch(
                    "voice_channel_move", member, before.channel, after.channel
                )

    @commands.Cog.listener()
    async def on_voice_channel_connect(self, member: Member, channel: VoiceChannel):
        if member == self.bot.user:
            return
        if self.bot.user in channel.members:
            player: Player = self.bot.players[channel.guild.id]
            if player.stream and not player.playing:
                ctx = player.context
                await self.bot.get_cog("Music").resume(context=ctx)

    @commands.Cog.listener()
    async def on_voice_channel_alone(self, member: Member, channel: VoiceChannel):
        if channel.members[0].id == self.bot.user.id:
            player: Player = self.bot.players[channel.guild.id]
            if player.playing:
                ctx = player.context
                await self.bot.get_cog("Music").pause(context=ctx)


def setup(bot):
    bot.add_cog(VoiceHandler(bot))
