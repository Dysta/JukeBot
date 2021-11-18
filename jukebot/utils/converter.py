import re


def seconds_to_time(seconds: int) -> (int, int, int, int):
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    d, h = divmod(h, 24)
    return d, h, m, s


def time_to_youtube_format(time: (int, int, int, int)) -> str:
    return re.sub(r"^[0:]*(.+:..)$", r"\1", ":".join([f"{e:02d}" for e in time]))


def seconds_to_youtube_format(seconds: int) -> str:
    return time_to_youtube_format(seconds_to_time(seconds))


def number_to_str(n: int) -> str:
    number: dict = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "keycap_ten",
    }
    return number[n]


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


def emoji_to_number(e: str) -> int:
    emoji: dict = {
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
        "5️⃣": 5,
        "6️⃣": 6,
        "7️⃣": 7,
        "8️⃣": 8,
        "9️⃣": 9,
        "🔟": 10,
    }
    return emoji[e]
