from abc import ABC, abstractmethod
from typing import Union


class EventStorage(ABC):
    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def get(self):
        pass

    @abstractmethod
    async def update(self):
        pass

    @abstractmethod
    async def delete(self):
        pass
