import re


URL_REGEX = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"
URL_PATTERN = re.compile(URL_REGEX, re.MULTILINE)


def is_url(s: str) -> bool:
    return not URL_PATTERN.match(s) is None
