from functools import lru_cache

from fastapi import Depends

from db.event_storage import get_storage, EventStorage


class MoviesService:

    def __init__(self, storage):
        self.storage: EventStorage = storage

    async def save_movie_progress(self, movie_id: str, user_id: str, viewed_frame: str) -> None:
        await self.storage.save(
            document="movies_progress",
            key=movie_id+user_id,
            value={
                "user_id": user_id,
                "movie_id": movie_id,
                "viewed_frame": viewed_frame
            }
        )


@lru_cache(maxsize=128)
def get_movies_service(storage: EventStorage = Depends(get_storage)) -> MoviesService:
    return MoviesService(storage)
