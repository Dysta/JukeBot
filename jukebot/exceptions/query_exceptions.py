from __future__ import annotations

from typing import Optional

from disnake.ext.commands import CommandError


class QueryException(CommandError):
    def __init__(
        self,
        message: str,
        *,
        query: Optional[str] = None,
        full_query: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.query: Optional[str] = query
        self.full_query: Optional[str] = full_query


class QueryFailed(QueryException):
    pass


class QueryCanceled(QueryException):
    pass
