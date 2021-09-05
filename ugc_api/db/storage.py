from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = None


async def connect_db(host, port):
    """Create database connection."""
    global client
    client = AsyncIOMotorClient(host, port)


async def close_db():
    """Close database connection."""
    client.close()


class Storage(ABC):
    def __call__(self):
        return self

    @abstractmethod
    async def create(self, document: dict):
        pass

    @abstractmethod
    async def get(self, spec: dict):
        """Get a single document from the database."""
        pass

    @abstractmethod
    async def find(self, spec: dict, length: int):
        """The filter argument is a prototype document that all results must match."""
        pass

    @abstractmethod
    async def update(self, spec: dict, document: dict,):
        pass

    @abstractmethod
    async def delete(self, spec: dict):
        pass


class AsyncMongoStorage(Storage):
    def __init__(self, db: str, collection: str):
        super().__init__()
        self.db = db
        self.collection = collection

    async def create(self, document: dict) -> dict:
        return await client[self.db][self.collection].insert_one(document)

    async def get(self, spec: dict) -> dict:
        return await client[self.db][self.collection].find_one(spec)

    async def find(self, spec: dict, length: int) -> dict:
        return await client[self.db][self.collection].find(spec).to_list(length)

    async def update(self, spec: dict, document: dict):
        updated = await client[self.db][self.collection].update_one(spec, document)
        return updated.matched_count > 0

    async def delete(self, spec: dict):
        return await client[self.db][self.collection].delete_one(spec)


def get_current_storage(**kwargs) -> Storage:
    return AsyncMongoStorage(**kwargs)
