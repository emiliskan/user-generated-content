from functools import lru_cache

from fastapi import Depends
from db import Storage, get_current_storage
from services.base import BaseService
from models import UserBookmarks


class UserBookmarksService(BaseService):
    async def add(self, user_id, movie_id):
        old_bookmarks = await self.storage.get({"_id": user_id})
        if old_bookmarks:
            if old_bookmarks["bookmarks"] is None:
                bookmarks = [movie_id]
            else:
                bookmarks = set(old_bookmarks["bookmarks"])
                bookmarks.add(movie_id)
            updated = await self.storage.update({"_id": user_id}, {"$set": {"bookmarks": list(bookmarks)}})
            return updated
        bookmarks = [movie_id]
        created = await self.storage.create({"_id": user_id, "bookmarks": bookmarks})
        return created

    async def remove(self, user_id, movie_id):
        old_bookmarks = await self.storage.get({"_id": user_id})
        if old_bookmarks and old_bookmarks["bookmarks"] is not None:
            bookmarks = old_bookmarks["bookmarks"]
            bookmarks.remove(movie_id)
            updated = await self.storage.update({"_id": user_id}, {"$set": {"bookmarks": bookmarks}})
            return updated
        raise Exception("Bookmark doesn't exist")

    async def get(self, user_id):
        old_bookmarks = await self.storage.get({"_id": user_id})
        return old_bookmarks


@lru_cache()
def get_user_bookmarks_service(
        storage: Storage = Depends(get_current_storage),
) -> UserBookmarksService:
    return UserBookmarksService(UserBookmarks, storage)
