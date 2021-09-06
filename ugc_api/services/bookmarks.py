from functools import lru_cache

from fastapi import Depends
from db import Storage, get_current_storage
from services.base import BaseService
from models import UserBookmarks


class UserBookmarksService(BaseService):
    async def add(self, user_id, movie_id):
        updated = await self.storage.update({"_id": user_id}, {"$addToSet": {"bookmarks": movie_id}})
        return updated

    async def remove(self, user_id, movie_id):
        updated = await self.storage.update({"_id": user_id}, {"$pull": {"bookmarks": movie_id}})
        return updated

    async def get(self, user_id):
        bookmarks = await self.storage.get({"_id": user_id})
        return bookmarks


@lru_cache()
def get_user_bookmarks_service(
        storage: Storage = Depends(get_current_storage(db="ugc_db", collection="user_bookmarks")),
) -> UserBookmarksService:
    return UserBookmarksService(UserBookmarks, storage)
