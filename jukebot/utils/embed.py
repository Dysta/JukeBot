from __future__ import annotations

import itertools
import random
from typing import TYPE_CHECKING, Union

import disnake
from disnake import Member

from jukebot.utils import converter

if TYPE_CHECKING:
    from jukebot.components import Result, ResultSet, Song

VOID_TOKEN = "\u200B"


def _base_embed(content="", color=0x38383D):
    return disnake.Embed(title="", description=content, color=color)


def error_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0xDB3C30)
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-error-icon.png",
    )
    return embed


def info_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0x30A3DB)

    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-information-icon.png",
    )
    return embed


def basic_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0x4F4F4F)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://cdn.discordapp.com/attachments/573225654452092930/908327963718713404/juke-icon.png",
    )
    return embed


def activity_message(title="", content=""):
    colors = [0xF6C333, 0xF4B400]
    c = colors[random.randint(0, 1)]
    embed: disnake.Embed = _base_embed(content=content, color=c)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/dragon-ball-online-global-icon.png",
    )
    return embed


def music_message(song: Song, current_duration: int = 0):
    colors = [0x736DAB, 0xFFBA58]
    c = colors[random.randint(0, 1)]

    embed: disnake.Embed = _base_embed(content="", color=c)
    embed.set_author(
        name=song.title,
        url=song.web_url,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/musicbrainz-icon.png",
    )
    embed.add_field(name="Channel", value=song.channel, inline=bool(len(song.title) >= 40))
    if current_duration:
        line = converter.duration_seconds_to_progress_bar(current_duration, song.duration)
        fmt_current: str = converter.seconds_to_youtube_format(current_duration)
        embed.add_field(name="Progression", value=f"`{fmt_current} {line} {song.fmt_duration}`")
    else:
        embed.add_field(name="Duration", value=song.fmt_duration)
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    return embed


def music_search_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0x4F4F4F)
    embed.set_author(
        name="Search" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/d-feet-icon.png",
    )
    return embed


def music_not_found_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0xEBA229)
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/plasma-search-icon.png",
    )
    return embed


def music_found_message(music: dict, title=""):
    embed: disnake.Embed = _base_embed(content=f"[{music['title']}]({music['url']})", color=0x54B23F)
    embed.set_author(
        name="Music found!" if title == "" else title,
        icon_url="https://cdn.discordapp.com/attachments/573225654452092930/952197615221612594/d-feet-icon.png",
    )
    embed.set_thumbnail(url=music["image_url"])
    return embed


def search_result_message(playlist: ResultSet, title=""):
    content = "\n\n".join(
        [
            f"{converter.number_to_emoji(i)} `{s.title} by {s.channel}` **[{s.fmt_duration}]**"
            for i, s in enumerate(playlist, start=1)
        ]
    )
    embed: disnake.Embed = music_search_message(title=title, content=content)
    embed.add_field(
        name=VOID_TOKEN,
        value="Use the selector below to choose a result.",
    )
    return embed


def basic_queue_message(title="", content=""):
    colors = [0x438F96, 0x469961, 0x3F3F3F]
    c = colors[random.randint(0, 2)]
    embed: disnake.Embed = _base_embed(content=content, color=c)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/logisim-icon-icon.png",
    )
    return embed


def queue_message(playlist: ResultSet, title=""):
    playlist_slice = itertools.islice(playlist, 10)
    content = "\n\n".join(
        [
            f"`{i}` • `{s.title}` on `{s.channel}` **[{s.fmt_duration}]** — `{s.requester}`"
            for i, s in enumerate(playlist_slice, start=1)
        ]
    )
    embed: disnake.Embed = basic_queue_message(title=title, content=content)
    embed.add_field(name="Total songs", value=f"`{len(playlist)}`")
    total_time: int = sum([e.duration for e in playlist if not e.live])
    total_time_fmt: str = converter.seconds_to_youtube_format(total_time)
    embed.add_field(name="Total duration", value=f"`{total_time_fmt}`")
    embed.add_field(
        name=VOID_TOKEN,
        value=f"Use command `add` or `remove` to add or remove a song.",
        inline=False,
    )
    return embed


def result_enqueued(res: Result):
    colors = [0x438F96, 0x469961, 0x3F3F3F]
    c = colors[random.randint(0, 2)]
    embed: disnake.Embed = _base_embed(content="", color=c)
    embed.set_author(
        name=f"Enqueued : {res.title}",
        url=res.web_url,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/logisim-icon-icon.png",
    )
    embed.add_field(name="Channel", value=res.channel, inline=True)
    embed.add_field(name="Duration", value=res.fmt_duration)
    return embed


def grab_message(song: Song, current_duration: int = 0):
    embed: disnake.Embed = _base_embed(content=f"[{song.title}]({song.web_url})", color=0x366ADB)
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
    embed: disnake.Embed = _base_embed(content=content, color=0x366ADB)
    embed.set_author(
        name=title if title else f"Music shared by {author}",
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/atunes-icon.png",
        url=url,
    )
    if img:
        embed.set_thumbnail(url=img)
    return embed
