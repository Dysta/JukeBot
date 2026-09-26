from __future__ import annotations

import random

import disnake

from .base import _base_embed


def activity_message(title="", content=""):
    colors = [0xF6C333, 0xF4B400]
    c = colors[random.randint(0, 1)]
    embed: disnake.Embed = _base_embed(content=content, color=c)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/dragon-ball-online-global-icon.png",
    )
    return embed
