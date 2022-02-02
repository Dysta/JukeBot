from nextcord import VoiceClient
from nextcord.ext.commands import Context, CheckFailure

from jukebot.components import Player


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


def bot_is_playing(ctx: Context):
    player: Player = ctx.bot.players[ctx.guild.id]
    if not player.is_playing:
        raise CheckFailure("The bot is not currently playing.")
    return True


def bot_is_not_playing(ctx: Context):
    player: Player = ctx.bot.players[ctx.guild.id]
    if player.is_playing:
        raise CheckFailure("The bot is already playing.")
    return True


def bot_is_streaming(ctx: Context):
    player: Player = ctx.bot.players[ctx.guild.id]
    if not player.is_streaming:
        raise CheckFailure("The bot is not currently playing.")
    return True


def bot_not_playing_live(ctx: Context):
    player: Player = ctx.bot.players[ctx.guild.id]
    if player.is_playing and player.song.live:
        raise CheckFailure("The bot is playing a live audio.")
    return True
