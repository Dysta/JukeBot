from disnake.ext.commands import CommandError


class PlayerException(CommandError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PlayerConnexionException(PlayerException):
    pass
