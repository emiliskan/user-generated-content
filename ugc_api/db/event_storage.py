""" Модуль для работы с хранилищем событий. """

from typing import Union, Optional
from abc import ABC, abstractmethod
import json

from aiokafka import AIOKafkaProducer


class EventStorage(ABC):
    """ Абстрактный класс для хранилищ. """

    @abstractmethod
    async def save(self, document: str, key: str, value: Union[str, dict]) -> None:
        """
        Функция записи в хранилище.

        :param document: Документ записи.
        :param key: Ключ записи.
        :param value: Значение записи.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Закрывает соединение с хранилищем.
        """
        pass


class KafkaStorage(EventStorage):
    """ Хранилище Kafka. """

    def __init__(self, producer: AIOKafkaProducer):
        self.producer: AIOKafkaProducer = producer

    async def save(self, document: str, key: str, value: Union[str, dict]) -> None:
        await self.producer.start()
        await self.producer.send_and_wait(
            topic=document,
            key=str.encode(key, "utf-8"),
            value=str.encode(json.dumps(value), "utf-8")
        )

    def close(self) -> None:
        self.producer.stop()


storage: Union[EventStorage, None] = None


def get_storage() -> Optional[EventStorage]:
    """ Текущее хранилище событий """
    return storage
