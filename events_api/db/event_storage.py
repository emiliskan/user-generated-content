import json
from abc import ABC, abstractmethod
from typing import Union

from kafka import KafkaProducer



class EventStorage(ABC):
    """ Абстрактный класс для хранилищ """

    @abstractmethod
    def save(self, document: str, key: str, value: Union[str, dict]) -> None:
        """
        Функция записи в хранилище
        :param document: Документ записи
        :param key: Ключ записи
        :param value: Значение записи
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Закрывает соединение с хранилищем
        """
        pass


class KafkaStorage(EventStorage):
    """ Хранилище Kafka"""

    def __init__(self, producer: KafkaProducer):
        self.producer: KafkaProducer = producer

    def save(self, document: str, key: str, value: Union[str, dict]) -> None:
        self.producer.send(
            topic=document,
            key=str.encode(key, "utf-8"),
            value=str.encode(json.dumps(value), "utf-8")
        )

    def close(self) -> None:
        self.producer.close()


storage: Union[EventStorage, None] = None


def get_storage() -> EventStorage:
    return storage



