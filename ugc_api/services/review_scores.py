from functools import lru_cache
from uuid import UUID
from typing import ClassVar
from bson import ObjectId

from fastapi import Depends

from db import Storage, get_current_storage
from services.base import BaseService
from models.base import PydanticObjectId
from models import ReviewScore
from services.exceptions import DocumentNotFound, NotAllowed
from services.reviews import get_user_reviews_service
from utils.misc import inc_avg_mean


class UserReviewScoresService(BaseService):

    def __init__(self, model: ClassVar, reviews_scores: Storage, reviews: Storage):
        super().__init__(model, reviews_scores)
        self.reviews = reviews

    async def get(self, review_score_id: ObjectId) -> dict:
        review = await self.storage.get({"_id": review_score_id})
        if not review:
            raise DocumentNotFound

        return review

    async def add(self, user_id: UUID, review_score: ReviewScore) -> dict:
        data = review_score.dict()
        data["user_id"] = user_id
        created = await self.storage.create(data)
        created = await self.get(created.inserted_id)

        review = await self.reviews.get({"_id": data["review_id"]})
        if review is None:
            raise DocumentNotFound

        old_rating = review.get("rating")
        scores_quality = review.get("scores_quality")
        new_rating = inc_avg_mean(old_rating, scores_quality, data["score"])

        review_data = {
            "$addToSet": {"scores": created["id"]},
            "$inc": {"scores_quality": 1},
            "$set": {"rating": new_rating}
        }

        await self.reviews.update({"_id": data["review_id"]}, review_data)

        return created

    async def update(self, user_id: UUID, review_score_id: PydanticObjectId, review_score: ReviewScore) -> None:

        data = review_score.dict()
        data["user_id"] = user_id
        review_score = await self.get(review_score_id)

        if not review_score["user_id"] == user_id:
            raise NotAllowed

        await self.storage.update({"_id": review_score_id}, {"$set": data})

        review = await self.reviews.get({"_id": data["review_id"]})
        if review is None:
            raise DocumentNotFound

        length = review["scores_quality"]
        scores = await self.storage.search({"review_id": review["_id"]},
                                          limit=length)
        new_rating = sum(s["score"] for s in scores) / length

        review_data = {
            "$set": {"rating": new_rating}
        }

        await self.reviews.update({"_id": review["_id"]}, review_data)

    async def remove(self, user_id: UUID, review_score_id: PydanticObjectId) -> None:
        review_score = await self.get(review_score_id)

        if not review_score["user_id"] == user_id:
            raise NotAllowed
        await self.storage.delete({"_id": review_score_id})

        review = await self.reviews.get({"_id": review_score["review_id"]})

        length = review["scores_quality"] - 1
        if length == 0:
            new_rating = 0
        else:
            scores = await self.storage.search({"review_id": review["_id"]},
                                               limit=length)
            new_rating = sum(s["score"] for s in scores) / length

        review_data = {
            "$pull": {"scores": review_score_id},
            "$inc": {"scores_quality": -1},
            "$set": {"rating": new_rating}
        }

        await self.reviews.update({"_id": review["_id"]}, review_data)


@lru_cache()
def get_user_review_scores_service(
        review_scores: Storage = Depends(get_current_storage(db='ugc_db', collection="review_scores")),
        reviews: Storage = Depends(get_current_storage(db='ugc_db', collection="reviews")),
) -> UserReviewScoresService:
    return UserReviewScoresService(ReviewScore, review_scores, reviews)
