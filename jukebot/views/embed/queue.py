from __future__ import annotations

import itertools
import random
from typing import TYPE_CHECKING

import disnake

from jukebot.utils import converter

from .base import _base_embed

if TYPE_CHECKING:
    from jukebot.components import Result, ResultSet


def basic_queue_message(title="", content=""):
    colors = [0x438F96, 0x469961, 0x3F3F3F]
    c = colors[random.randint(0, 2)]
    embed: disnake.Embed = _base_embed(content=content, color=c)
    embed.set_author(
        name="Information" if title == "" else title,
        icon_url="https://cdn.icon-icons.com/icons2/1381/PNG/512/xt7playermpv_94294.png",
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

    return embed


def result_enqueued(res: Result):
    colors = [0x438F96, 0x469961, OxF3F3F]
    c = colors[random.randint(0, 2)]
    embed: disnake.Embed = _base_embed(content="", color=c)
    embed.set_author(
        name=f"Enqueued : {res.title}",
        url=res.web_url,
        icon_url="https://cdn.icon-icons.com/icons2/1381/PNG/512/xt7playermpv_94294.png",
    )
    embed.add_field(name="Channel", value=res.channel, inline=True)
    embed.add_field(name="Duration", value=res.fmt_duration)
    return embed
