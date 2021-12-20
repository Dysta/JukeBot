from nextcord import VoiceClient
from nextcord.ext.commands import Context, CheckFailure


def user_is_connected(ctx: Context):
    if not ctx.message.author.voice:
        raise CheckFailure("You must be on a voice channel to use this command.")
    return True


def bot_is_connected(ctx: Context):
    if not ctx.guild.voice_client:
        raise CheckFailure("The bot is not connected to a voice channel.")
    return True


def bot_is_not_connected(ctx: Context):
    if ctx.guild.voice_client:
        raise CheckFailure("The bot is already connected to a voice channel.")
    return True


def bot_and_user_in_same_channel(ctx: Context):
    b_conn: bool = ctx.guild.voice_client
    u_conn: bool = ctx.message.author.voice
    if not b_conn or not u_conn:
        raise CheckFailure("You or the bot is not connected to a voice channel.")

    b_vc: VoiceClient = ctx.guild.voice_client.channel
    u_vc: VoiceClient = ctx.message.author.voice.channel
    if not b_vc == u_vc:
        raise CheckFailure("You're not connected to the same voice channel as the bot.")
    return True
