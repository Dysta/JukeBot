def seconds_converter(seconds: int) -> (int, int, int, int):
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    d, h = divmod(h, 24)
    return d, h, m, s
