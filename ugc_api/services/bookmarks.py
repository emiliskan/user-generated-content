from functools import lru_cache

from fastapi import Depends
from db import Storage, get_current_storage
from services.base import BaseService
from models import UserBookmarks


class UserBookmarksService(BaseService):
    async def add(self, user_id, movie_id):
        old_bookmarks = await self.storage.get({"_id": user_id})
        bookmarks = old_bookmarks["bookmarks"].push(movie_id)
        self.storage.update({"_id": user_id}, {"bookmarks": bookmarks})

    async def remove(self, user_id, movie_id):
        pass

    async def get(self, user_id):
        old_bookmarks = self.storage.get({"_id": user_id})
        return old_bookmarks["bookmarks"]


@lru_cache()
def get_user_bookmarks_service(
        storage: Storage = Depends(get_current_storage),
) -> UserBookmarksService:
    return UserBookmarksService(UserBookmarks, storage)
