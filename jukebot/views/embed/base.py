from __future__ import annotations

import disnake

VOID_TOKEN = "\u200b"


def _base_embed(content="", color=0x38383D):
    return disnake.Embed(title="", description=content, color=color)
