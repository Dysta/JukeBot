from nextcord import Embed, VoiceClient
from nextcord.ext.commands import Context

from jukebot.utils import embed


class VoiceChecks:
    @staticmethod
    async def user_is_connected(ctx: Context):
        if not ctx.message.author.voice:
            e: Embed = embed.error_message(
                ctx, content="You must be on a voice channel to use this command."
            )
            await ctx.send(embed=e)
            return False
        return True

    @staticmethod
    async def bot_is_connected(ctx: Context):
        if not ctx.guild.voice_client:
            e: Embed = embed.error_message(
                ctx, content="The bot is not connected to a voice channel."
            )
            await ctx.send(embed=e)
            return False
        return True

    @staticmethod
    async def bot_and_user_in_same_channel(ctx: Context):
        b_conn: bool = await VoiceChecks.bot_is_connected(ctx)
        u_conn: bool = await VoiceChecks.user_is_connected(ctx)
        if not b_conn or not u_conn:
            return False

        b_vc: VoiceClient = ctx.guild.voice_client.channel
        u_vc: VoiceClient = ctx.message.author.voice.channel
        if not b_vc == u_vc:
            e: Embed = embed.error_message(
                ctx,
                content="You're not connected to the same voice channel as the bot.",
            )
            await ctx.send(embed=e)
            return False
        return True
