import itertools

import nextcord
import random

from typing import Union
from nextcord.ext.commands import Context

from jukebot.components import Song, ResultSet, Result
from jukebot.components.songset import SongSet
from jukebot.utils import converter

VOID_TOKEN = "\u200B"


def error_message(ctx: Context, title="", content=""):
    embed: nextcord.Embed = nextcord.Embed(
        title="", description=content, color=0xDB3C30
    )
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-error-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.display_avatar.url}"
    )

    return embed


def info_message(ctx: Context, title="", content=""):
    embed: nextcord.Embed = nextcord.Embed(
        title="", description=content, color=0x30A3DB
    )
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-information-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.display_avatar.url}"
    )

    return embed


def basic_message(ctx: Context, title="", content=""):
    embed: nextcord.Embed = nextcord.Embed(
        title="", description=content, color=0x4F4F4F
    )
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://cdn.discordapp.com/attachments/573225654452092930/908327963718713404/juke-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.display_avatar.url}"
    )

    return embed


def music_message(ctx: Context, song: Song, current_duration: int = 0):
    colors = [0x736DAB, 0xFFBA58]
    c = colors[random.randint(0, 1)]
    embed: nextcord.Embed = nextcord.Embed(title="", description="", color=c)
    embed.set_author(
        name=song.title,
        url=song.web_url,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/musicbrainz-icon.png",
    )
    embed.add_field(
        name="Channel", value=song.channel, inline=bool(len(song.title) >= 40)
    )
    if current_duration:
        line = converter.duration_seconds_to_progress_bar(
            current_duration, song.duration
        )
        fmt_current: str = converter.seconds_to_youtube_format(current_duration)
        embed.add_field(
            name="Progression", value=f"`{fmt_current} {line} {song.fmt_duration}`"
        )
    else:
        embed.add_field(name="Duration", value=song.fmt_duration)
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.display_avatar.url}"
    )

    return embed


def music_search_message(ctx: Context, title="", content=""):
    embed: nextcord.Embed = nextcord.Embed(
        title="", description=content, color=0x4F4F4F
    )
    embed.set_author(
        name="Search" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/d-feet-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.display_avatar.url}"
    )

    return embed


def music_not_found_message(ctx: Context, title="", content=""):
    embed: nextcord.Embed = nextcord.Embed(
        title="", description=content, color=0xEBA229
    )
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/plasma-search-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar.url}"
    )

    return embed


def search_result_message(ctx: Context, playlist: Union[ResultSet, SongSet], title=""):
    content = "\n\n".join(
        [
            f"{converter.number_to_emoji(i)} `{s.title} by {s.channel}` **[{s.fmt_duration}]**"
            for i, s in enumerate(playlist, start=1)
        ]
    )
    embed: nextcord.Embed = music_search_message(ctx, title=title, content=content)
    embed.add_field(
        name=VOID_TOKEN,
        value="Use the selector below to choose a result.",
    )
    return embed


def basic_queue_message(ctx: Context, title="", content=""):
    colors = [0x438F96, 0x469961, 0x3F3F3F]
    c = colors[random.randint(0, 2)]
    embed: nextcord.Embed = nextcord.Embed(title="", description=content, color=c)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/logisim-icon-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.display_avatar.url}"
    )

    return embed


def queue_message(ctx: Context, playlist: Union[ResultSet, SongSet], title=""):
    playlist_slice = itertools.islice(playlist, 10)
    content = "\n\n".join(
        [
            f"{i}. `{s.title}` on `{s.channel}` **[{s.fmt_duration}]** — `{s.author}`"
            for i, s in enumerate(playlist_slice, start=1)
        ]
    )
    embed: nextcord.Embed = basic_queue_message(ctx, title=title, content=content)
    embed.add_field(name="Total songs", value=f"`{len(playlist)}`")
    total_time: int = sum([e.duration for e in playlist if not e.live])
    total_time_fmt: str = converter.seconds_to_youtube_format(total_time)
    embed.add_field(name="Total duration", value=f"`{total_time_fmt}`")
    return embed


def result_enqueued(ctx: Context, res: Result):
    colors = [0x438F96, 0x469961, 0x3F3F3F]
    c = colors[random.randint(0, 2)]
    embed: nextcord.Embed = nextcord.Embed(title="", description="", color=c)
    embed.set_author(
        name=f"Added to queue : {res.title}",
        url=res.web_url,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/logisim-icon-icon.png",
    )
    embed.add_field(name="Channel", value=res.channel, inline=True)
    embed.add_field(name="Duration", value=res.fmt_duration)
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.display_avatar.url}"
    )

    return embed
