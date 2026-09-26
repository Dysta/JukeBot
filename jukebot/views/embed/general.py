from __future__ import annotations

import disnake

from .base import _base_embed


def basic_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0x4F4F4F)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://cdn.discordapp.com/attachments/573225654452092930/908327963718713404/juke-icon.png",
    )
    return embed


def info_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0x30A3DB)

    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-information-icon.png",
    )
    return embed


def error_message(title="", content=""):
    embed: disnake.Embed = _base_embed(content=content, color=0xDB3C30)
    embed.set_author(
        name="Error" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-error-icon.png",
    )
    return embed
