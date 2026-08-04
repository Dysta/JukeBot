from __future__ import annotations

from disnake.ext.commands import CommandError


class QueryException(CommandError):
    def __init__(self, message: str, *, query: str | None = None, full_query: str | None = None) -> None:
        super().__init__(message)
        self.query: str | None = query
        self.full_query: str | None = full_query


class QueryFailed(QueryException):
    pass


class QueryCanceled(QueryException):
    pass
