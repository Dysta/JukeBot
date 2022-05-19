from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import CommandInteraction, VoiceClient
from disnake.ext.commands import CheckFailure

if TYPE_CHECKING:
    from jukebot.components import Player


def user_is_connected(inter: CommandInteraction):
    if not inter.author.voice:
        raise CheckFailure("You must be on a voice channel to use this command.")
    return True


def bot_is_connected(inter: CommandInteraction):
    if not inter.guild.voice_client:
        raise CheckFailure("The bot is not connected to a voice channel.")
    return True


def bot_is_not_connected(inter: CommandInteraction):
    if inter.guild.voice_client:
        raise CheckFailure("The bot is already connected to a voice channel.")
    return True


def bot_and_user_in_same_channel(inter: CommandInteraction):
    b_conn: bool = inter.guild.voice_client
    u_conn: bool = inter.author.voice
    if not b_conn or not u_conn:
        raise CheckFailure("You or the bot is not connected to a voice channel.")

    b_vc: VoiceClient = inter.guild.voice_client.channel
    u_vc: VoiceClient = inter.author.voice.channel
    if not b_vc == u_vc:
        raise CheckFailure("You're not connected to the same voice channel as the bot.")
    return True


def bot_is_playing(inter: CommandInteraction):
    player: Player = inter.bot.players[inter.guild.id]
    if not player.is_playing:
        raise CheckFailure("The bot is not currently playing.")
    return True


def bot_is_not_playing(inter: CommandInteraction):
    player: Player = inter.bot.players[inter.guild.id]
    if player.is_playing:
        raise CheckFailure("The bot is already playing.")
    return True


def bot_is_streaming(inter: CommandInteraction):
    player: Player = inter.bot.players[inter.guild.id]
    if not player.is_streaming:
        raise CheckFailure("The bot is not currently playing.")
    return True


def bot_not_playing_live(inter: CommandInteraction):
    player: Player = inter.bot.players[inter.guild.id]
    if player.is_playing and player.song.live:
        raise CheckFailure("The bot is playing a live audio.")
    return True
