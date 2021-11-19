import discord
import random

from typing import Union
from discord.ext.commands import Context

from jukebot.components import Song, ResultSet
from jukebot.components.songset import SongSet
from jukebot.utils import converter

VOID_TOKEN = "\u200B"


def error_message(ctx: Context, title="", content=""):
    embed: discord.Embed = discord.Embed(title="", description=content, color=0xDB3C30)
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-error-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
    )

    return embed


def info_message(ctx: Context, title="", content=""):
    embed: discord.Embed = discord.Embed(title="", description=content, color=0x30A3DB)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-information-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
    )

    return embed


def basic_message(ctx: Context, title="", content=""):
    embed: discord.Embed = discord.Embed(title="", description=content, color=0x4F4F4F)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://cdn.discordapp.com/attachments/573225654452092930/908327963718713404/juke-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
    )

    return embed


def music_message(ctx: Context, song: Song, current_duration: int = 0):
    colors = [0x736DAB, 0xFFBA58]
    c = colors[random.randint(0, 1)]
    embed: discord.Embed = discord.Embed(title="", description="", color=c)
    embed.set_author(
        name=song.title,
        url=song.web_url,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/musicbrainz-icon.png",
    )
    embed.add_field(
        name="Channel", value=song.channel, inline=bool(len(song.title) >= 40)
    )
    if current_duration:
        fmt_current: str = converter.seconds_to_youtube_format(current_duration)
        embed.add_field(
            name="Progression", value=f"{fmt_current} / {song.fmt_duration}"
        )
    else:
        embed.add_field(name="Duration", value=song.fmt_duration)
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
    )

    return embed


def music_search_message(ctx: Context, title="", content=""):
    embed: discord.Embed = discord.Embed(title="", description=content, color=0x4F4F4F)
    embed.set_author(
        name="Search" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/d-feet-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
    )

    return embed


def music_not_found_message(ctx: Context, title="", content=""):
    embed: discord.Embed = discord.Embed(title="", description=content, color=0xEBA229)
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/plasma-search-icon.png",
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
    )

    return embed


def playlist_message(ctx: Context, playlist: Union[ResultSet, SongSet], title=""):
    content = "\n\n".join(
        [
            f":{converter.number_to_str(i)}: `{s.title} by {s.channel}` **[{s.fmt_duration}]**"
            for i, s in enumerate(playlist, start=1)
        ]
    )
    embed: discord.Embed = music_search_message(ctx, title=title, content=content)
    embed.add_field(
        name=VOID_TOKEN,
        value="Click on the reaction corresponding to the emoji. Click on ❌ to cancel the research.",
    )
    return embed
