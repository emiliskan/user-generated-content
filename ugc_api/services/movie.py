from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from core.config import MONGO_DB
from db import Storage, get_current_storage
from models import Movie
from services.base import BaseService
from services.exceptions import DocumentNotFound


class MovieService(BaseService):
    async def get(self, movie_id: UUID):
        result = await self.storage.get({"_id": movie_id})
        if not result:
            raise DocumentNotFound

        return result


@lru_cache()
def get_movie_service(
        storage: Storage = Depends(get_current_storage(db=MONGO_DB,
                                                       collection="movies"))
) -> MovieService:
    return MovieService(Movie, storage)
