class AbstractService:
    def __init__(self, bot):
        self.bot = bot

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): ...
