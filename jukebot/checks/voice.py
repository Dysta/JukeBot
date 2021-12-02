from nextcord import Embed, VoiceClient
from nextcord.ext.commands import Context

from jukebot.utils import embed


class VoiceChecks:
    @staticmethod
    async def user_is_connected(ctx: Context):
        if not ctx.message.author.voice:
            e: Embed = embed.error_message(
                ctx.author, content="You must be on a voice channel to use this command."
            )
            await ctx.send(embed=e)
            return False
        return True

    @staticmethod
    async def bot_is_connected(ctx: Context):
        if not ctx.guild.voice_client:
            e: Embed = embed.error_message(
                ctx.author, content="The bot is not connected to a voice channel."
            )
            await ctx.send(embed=e)
            return False
        return True

    @staticmethod
    async def bot_is_not_connected(ctx: Context):
        if ctx.guild.voice_client:
            e: Embed = embed.error_message(
                ctx.author, content="The bot is already connected to a voice channel."
            )
            await ctx.send(embed=e)
            return False
        return True

    @staticmethod
    async def bot_and_user_in_same_channel(ctx: Context):
        b_conn: bool = ctx.guild.voice_client
        u_conn: bool = ctx.message.author.voice
        if not b_conn or not u_conn:
            return False

        b_vc: VoiceClient = ctx.guild.voice_client.channel
        u_vc: VoiceClient = ctx.message.author.voice.channel
        if not b_vc == u_vc:
            e: Embed = embed.error_message(
                ctx.author,
                content="You're not connected to the same voice channel as the bot.",
            )
            await ctx.send(embed=e)
            return False
        return True
