import ssl
from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = None


async def connect_db(host, port, ssl_ca_certs: str, user: str, password: str):
    """Create database connection."""
    global client
    client = AsyncIOMotorClient(
        host=host,
        port=port,
        ssl_ca_certs=ssl_ca_certs,
        ssl_cert_reqs=ssl.CERT_OPTIONAL,
        username=user,
        password=password
    )


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

    async def create(self, document: dict):
        return await client[self.db][self.collection].insert_one(document)

    async def get(self, spec: dict):
        return await client[self.db][self.collection].find_one(spec)

    async def update(self, spec: dict, document: dict):
        updated = await client[self.db][self.collection].update_one(spec, document)
        return updated.matched_count > 0

    async def delete(self, spec: dict):
        return await client[self.db][self.collection].delete_one(spec)


def get_current_storage(**kwargs) -> Storage:
    return AsyncMongoStorage(**kwargs)
