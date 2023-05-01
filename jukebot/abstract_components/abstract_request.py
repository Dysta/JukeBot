from abc import ABC, abstractmethod
from typing import Any


class AbstractRequest(ABC):
    """Class that represent a request made by the user during a command."""

    def __init__(self, query: str) -> None:
        self._query: str = query
        self._result: Any = None
        self._success: bool = False

    @abstractmethod
    async def setup(self):
        """Setup the Request. Called before the execute method."""

    @abstractmethod
    async def execute(self):
        """Execute the Request and handle the result type"""

    @abstractmethod
    async def terminate(self):
        """Cleanup the Request. Called after the execute method."""

    async def __aenter__(self):
        await self.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.terminate()

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
