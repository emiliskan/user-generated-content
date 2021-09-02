from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION


class Storage(ABC):
    def __call__(self):
        return self

    @abstractmethod
    def client(self):
        pass

    @abstractmethod
    async def create(self, document: dict):
        pass

    @abstractmethod
    async def get(self, spec: dict):
        pass

    @abstractmethod
    async def update(self, spec: dict, document: dict,):
        pass

    @abstractmethod
    async def delete(self, spec: dict):
        pass


storage: AsyncIOMotorClient = None


async def get_db_client() -> AsyncIOMotorClient:
    """Return database client instance."""
    return AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)


async def close_db():
    """Close database connection."""
    storage.close()


class AsyncMongoStorage(Storage):
    def __init__(self):
        super().__init__()
        self.db_name = MONGO_DB
        self.collection_name = MONGO_COLLECTION
        self.db_client = None

    async def _asyncinit(self):
        self.db_client = await get_db_client()
        self.collection = self.db_client[self.db_name][self.collection_name]

    async def create(self, document: dict):
        return await self.collection.insert_one(document)

    async def get(self, spec: dict):
        return await self.collection.find_one(spec)

    async def update(self, spec: dict, document: dict):
        updated = await self.collection.update_one(spec, document)
        return updated.matched_count > 0

    async def delete(self, spec: dict):
        return await self.collection.delete_one(spec)


async def get_current_storage() -> Storage:
    mongo_storage = AsyncMongoStorage()
    await mongo_storage._asyncinit()
    return mongo_storage

