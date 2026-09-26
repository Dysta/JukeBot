from __future__ import annotations

from typing import TYPE_CHECKING

from jukebot.utils import converter

from .base import _base_embed

if TYPE_CHECKING:
    from disnake import Embed, Member

    from jukebot.components import Song


def grab_message(song: Song, current_duration: int = 0):
    embed: Embed = _base_embed(content=f"[{song.title}]({song.web_url})", color=0x366ADB)
    embed.set_author(
        name="Saved music",
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/atunes-icon.png",
    )
    embed.add_field(name="Channel", value=song.channel)
    fmt_current: str = converter.seconds_to_youtube_format(current_duration)
    embed.add_field(name="Time code", value=f"`{fmt_current}/{song.fmt_duration}`")
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    return embed


def share_message(author: Member, content, title="", url="", img=""):
    embed: Embed = _base_embed(content=content, color=0x366ADB)
    embed.set_author(
        name=title if title else f"Music shared by {author}",
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/atunes-icon.png",
        url=url,
    )
    if img:
        embed.set_thumbnail(url=img)
    return embed
