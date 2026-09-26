from __future__ import annotations

import re

import yaml


def seconds_to_time(seconds: int) -> (int, int, int, int):
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    d, h = divmod(h, 24)
    return d, h, m, s


def time_to_youtube_format(time: (int, int, int, int)) -> str:
    return re.sub(r"^[0:]*(.+:..)$", r"\1", ":".join([f"{e:02d}" for e in time]))


def seconds_to_youtube_format(seconds: int) -> str:
    return time_to_youtube_format(seconds_to_time(seconds))


def number_to_emoji(n: int) -> str:
    number: dict = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟",
    }
    return number[n]


def duration_seconds_to_progress_bar(time: int, total: int, ticks: int = 30) -> str:
    x = int(ticks * (time / total)) if total else 0
    line = "".join(["▬" if t != x else "🔘" for t in range(ticks)])
    return line


def radios_yaml_to_dict() -> dict:
    radios: dict = {}
    with open("./data/radios.yaml", "r") as f:
        radios = yaml.safe_load(f)

    return radios
