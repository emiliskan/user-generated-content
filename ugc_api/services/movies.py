"""Модуль сервиса фильмов."""

from functools import lru_cache

from core.config import LRU_MAX_SIZE
from db.event_storage import EventStorage, get_storage
from fastapi import Depends


class MoviesService(object):
    """Сервис для работы с фильмами."""

    def __init__(self, storage: EventStorage) -> None:
        """
        Инициализация сервиса работы с фильмами.

        Parameters:
            storage: Хранилище для записи информации.
        """
        self.storage: EventStorage = storage

    async def save_movie_progress(self, movie_id: str, user_id: str, viewed_frame: str) -> None:
        """
        Сохраняет прогресс фильма.

        Parameters:
            movie_id: Идентификатор фильма.
            user_id: Идентификатор пользователя.
            viewed_frame: Номер просмотренного фрейма.
        """
        await self.storage.save(
            document='movies_progress',
            key=movie_id + user_id,
            value={
                'user_id': user_id,
                'movie_id': movie_id,
                'viewed_frame': viewed_frame,
            },
        )


@lru_cache(maxsize=LRU_MAX_SIZE)
def get_movies_service(
        storage: EventStorage = Depends(get_storage),
) -> MoviesService:
    """Кэшируемый возврат инстанса сервиса фильмов.

    Parameters:
        storage: Хранилище для записи информации.

    Returns:
        Сервис работы с фильмами.
    """
    return MoviesService(storage)
