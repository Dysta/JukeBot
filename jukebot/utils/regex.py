import re

URL_REGEX = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"
URL_PATTERN = re.compile(URL_REGEX, re.MULTILINE)

TO_SNAKE_REGEX = r"(?<!^)([A-Z])"
TO_SNAKE_PATTERN = re.compile(TO_SNAKE_REGEX, re.MULTILINE)


def is_url(s: str) -> bool:
    return not URL_PATTERN.match(s) is None


def to_snake(pascal_str: str) -> str:
    snake_str = re.sub(TO_SNAKE_PATTERN, r"_\1", pascal_str)
    return snake_str.lower()
