from __future__ import annotations

import random
from typing import TYPE_CHECKING

import disnake

from jukebot.utils import converter

from .base import VOID_TOKEN, _base_embed

if TYPE_CHECKING:
    from jukebot.components import Song
    from jukebot.components.player import Player


def music_message(song: Song, loop_mode: Player.Loop, current_duration: int = 0):
    colors = [0x736DAB, 0xFFBA58]
    c = colors[random.randint(0, 1)]

    embed: disnake.Embed = _base_embed(content="", color=c)
    embed.set_author(
        name=song.title,
        url=song.web_url,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/musicbrainz-icon.png",
    )

    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)

    embed.add_field(name="Channel", value=song.channel, inline=True)
    if current_duration:
        embed.add_field(VOID_TOKEN, VOID_TOKEN, inline=True)
    embed.add_field("Loop", loop_mode.name.capitalize(), inline=True)

    if current_duration:
        line = converter.duration_seconds_to_progress_bar(current_duration, song.duration)
        fmt_current: str = converter.seconds_to_youtube_format(current_duration)
        embed.add_field(name="Progression", value=f"`{fmt_current} {line} {song.fmt_duration}`")
    else:
        embed.add_field(name="Duration", value=f"`{song.fmt_duration}`")

    return embed
