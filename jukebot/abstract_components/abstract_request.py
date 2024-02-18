import contextlib
from typing import Any


class AbstractRequest(contextlib.AbstractAsyncContextManager):
    """Class that represent a request made by the user during a command."""

    def __init__(self, query: str) -> None:
        self._query: str = query
        self._result: Any = None
        self._success: bool = False

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def query(self) -> str:
        """Return the current query

        Returns
        -------
        str
            The current query
        """
        return self._query

    @property
    def result(self) -> Any:
        """Return the current result

        Returns
        -------
        Any
            The current result
        """
        return self._result

    @property
    def success(self) -> bool:
        """Return the current success

        Returns
        -------
        bool
            The current success
        """
        return self._success
