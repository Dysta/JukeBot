import re


def seconds_converter(seconds: int) -> (int, int, int, int):
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    d, h = divmod(h, 24)
    return d, h, m, s


def convert_time_to_youtube_format(time: (int, int, int, int)) -> str:
    return re.sub(r"^[0:]*(.+:..)$", r"\1", ":".join([f"{e:02d}" for e in time]))
