class AbstractService:
    """This class allow you to implement your own service and using it from the bot.
    To implement a service, create a new file in the `services` package then implement this class.
    Don't forget, services are named `XXXService` where `XXX` is your action.
    To register a service, go to the cog where it's used then in the setup function, add your service by using `bot.add_service(XXXService())`.
    To use a service: `bot.services.XXX` where `XXX` is your previous named action.
    """

    def __init__(self, bot):
        self.bot = bot

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): ...
