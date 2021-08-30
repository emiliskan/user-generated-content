from abc import ABC, abstractmethod
from typing import Union

from motor.motor_asyncio import AsyncIOMotorClient


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


class AsyncMongoStorage(Storage):
    def __init__(self, collection=''):
        super().__init__()
        self.collection = collection

    @property
    def client(self):
        return storage

    async def create(self, document: dict):
        return await self.client.insert_one(document)

    async def get(self, spec: dict):
        return await self.client.find(spec)

    async def update(self, spec: dict, document: dict):
        return await self.client.update(spec, document)

    async def delete(self, spec: dict):
        return await self.client.delete_one(spec)


def get_current_storage(**kwargs) -> Storage:
    return AsyncMongoStorage(**kwargs)
