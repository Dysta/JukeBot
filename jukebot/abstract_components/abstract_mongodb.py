from motor.motor_asyncio import AsyncIOMotorClient


class AbstractMongoDB:
    _instance = None

    def __init__(self, **kwargs):
        self._db = self._client[kwargs.get("database")]
        self._collection = self._db[kwargs.get("collection")]

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super(AbstractMongoDB, cls).__new__(cls)
            cls._client = AsyncIOMotorClient(kwargs.get("url"))
        return cls._instance

    async def len(self) -> int:
        return await self._collection.count_documents({})
