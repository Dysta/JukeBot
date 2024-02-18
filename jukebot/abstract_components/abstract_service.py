from __future__ import annotations

import contextlib

from disnake import CommandInteraction


class AbstractService(contextlib.AbstractAsyncContextManager, contextlib.AbstractContextManager):
    """Abstract class for all services. A service can be async or not."""

    def __init__(self, bot, interaction: CommandInteraction):
        """
        Initialize the object with the provided bot and interaction.

        Args:
            bot: The bot object.
            interaction: The CommandInteraction object.
        """
        self.bot = bot
        self.interaction = interaction

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Allow the service to be instanciated with an async context manager."""
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        """Allow the service to be instanciated with a context manager."""
        return None
