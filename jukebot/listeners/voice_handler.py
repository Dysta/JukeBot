from nextcord import Member, VoiceState, VoiceChannel
from nextcord.ext import commands
from nextcord.ext.commands import Bot

from jukebot.components import PlayerCollection, Player


class VoiceHandler(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self._players: PlayerCollection = PlayerCollection(bot)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        # TODO: FINIR
        channel: VoiceChannel = before.channel or after.channel
        print(f"{channel.members=}")
        print(f"{len(channel.members)=}")
        # if len(channel.members) == 1 and sum(1 for m in channel.members if m.bot):
        #     player: Player = self._players[channel.guild.id]
        #     player.pause()


def setup(bot):
    bot.add_cog(VoiceHandler(bot))
