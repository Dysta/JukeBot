from __future__ import annotations

from typing import TYPE_CHECKING

from jukebot.utils import converter

from .base import VOID_TOKEN, _base_embed

if TYPE_CHECKING:
    from disnake import Embed

    from jukebot.components import ResultSet


def music_search_message(title="", content=""):
    embed: Embed = _base_embed(content=content, color=0x4F4F4F)
    embed.set_author(
        name="Search" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/d-feet-icon.png",
    )
    return embed


def search_result_message(playlist: ResultSet, title=""):
    content = "\n\n".join(
        [
            f"{converter.number_to_emoji(i)} `{s.title} by {s.channel}` **[{s.fmt_duration}]**"
            for i, s in enumerate(playlist, start=1)
        ]
    )
    embed: Embed = music_search_message(title=title, content=content)
    embed.add_field(
        name=VOID_TOKEN,
        value="Use the selector below to choose a result.",
    )
    return embed


def music_found_message(music: dict, title=""):
    links = " | ".join(f"[{name}]({url})" for name, url in music["links"].items())
    embed: Embed = _base_embed(color=0x54B23F)
    embed.set_author(
        name="Music found!" if title == "" else title,
        icon_url="https://cdn.discordapp.com/attachments/573225654452092930/952197615221612594/d-feet-icon.png",
    )
    title = f"[{music['title']}]({music['url']})" if music["url"] else music["title"]
    embed.add_field(name="Title", value=title, inline=False)
    embed.add_field(name="Artist", value=music["author"], inline=True)
    embed.add_field(name=VOID_TOKEN, value=VOID_TOKEN, inline=True)
    embed.add_field(name="Links", value=links, inline=True)
    if isinstance(music["image_url"], str) and music["image_url"].startswith(("http://", "https://")):
        embed.set_thumbnail(url=music["image_url"])
    return embed


def music_not_found_message(title="", content=""):
    embed: Embed = _base_embed(content=content, color=0xEBA229)
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/plasma-search-icon.png",
    )
    return embed
