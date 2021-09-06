from functools import lru_cache
from uuid import UUID
from fastapi import Depends

from models.base import PydanticObjectId
from services.exceptions import DocumentNotFound, NotAllowed
from db import Storage, get_current_storage
from services.base import BaseService
from models import Review, ReviewQuery


class UserReviewsService(BaseService):

    async def get(self, review_id: PydanticObjectId):
        review = await self.storage.get({"_id": review_id})
        if not review:
            raise DocumentNotFound

        return review

    async def search(self, query: ReviewQuery):
        reviews = await self.storage.search(
            filters=query.filters,
            offset=query.offset,
            limit=query.limit
        )

        if not reviews:
            return []

        return reviews

    async def add(self, user_id: UUID, review: Review):
        data = review.dict()
        data["user_id"] = user_id
        created = await self.storage.create(data)
        return await self.get(created.inserted_id)

    async def update(self, user_id: UUID, review_id: PydanticObjectId, review: Review):
        data = review.dict()
        await self.storage.update({"_id": review_id}, {"$set": data})
        return await self.get(review_id)

    async def remove(self, user_id: UUID, review_id: PydanticObjectId):
        review = await self.get(review_id)

        if not review["user_id"] == user_id:
            raise NotAllowed

        deleted = await self.storage.delete({"_id": review_id})
        return deleted


@lru_cache()
def get_user_reviews_service(
        storage: Storage = Depends(get_current_storage(db='ugc_db', collection="reviews")),
) -> UserReviewsService:
    return UserReviewsService(Review, storage)
