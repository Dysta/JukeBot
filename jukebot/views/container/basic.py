from __future__ import annotations

from disnake import ui


def basic_message(title: str, content: str | list[str] | None = None) -> ui.Container:
    if content is None:
        return ui.Container(
            ui.TextDisplay(f"### {title}"),
        )

    content = content if isinstance(content, list) else [content]
    txt_content = [ui.TextDisplay(f"-# {c}") if c != "" else ui.Separator() for c in content]
    return ui.Container(
        ui.TextDisplay(f"### {title}"),
        ui.Separator(),
        *txt_content,
    )
