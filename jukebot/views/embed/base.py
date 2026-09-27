from __future__ import annotations

from disnake import Embed

VOID_TOKEN = "\u200b"


def _base_embed(content="", color=0x38383D) -> Embed:
    return Embed(title="", description=content, color=color)
