from functools import lru_cache
from uuid import UUID
from typing import ClassVar

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

    async def get(self, review_score_id: PydanticObjectId) -> dict:
        review = await self.storage.get({"_id": review_score_id})
        if not review:
            raise DocumentNotFound

        return review

    async def update_review_score(self, score_id: PydanticObjectId, review_score: dict, score_inc: int):
        review = await self.reviews.get({"_id": review_score["review_id"]})
        old_rating = review.get("rating")
        scores_quality = review.get("scores_quality")
        new_rating = inc_avg_mean(old_rating, scores_quality, review_score["score"])

        review_data = {
            "$addToSet": {"scores": score_id},
            "$inc": {"scores_quality": score_inc},
            "$set": {"rating": new_rating}
        }
        await self.reviews.update({"_id": review_score["review_id"]}, review_data)

    async def add(self, user_id: UUID, review_score: ReviewScore) -> None:
        data = review_score.dict()
        data["user_id"] = user_id
        created = await self.storage.create(data)
        created = await self.get(created.inserted_id)
        await self.update_review_score(created["_id"], data, 1)

    async def remove(self, user_id: UUID, review_score_id: PydanticObjectId) -> None:
        review_score = await self.get(review_score_id)

        if not review_score["user_id"] == user_id:
            raise NotAllowed

        await self.update_review_score(review_score_id, review_score, -1)
        await self.storage.delete({"_id": review_score_id})


@lru_cache()
def get_user_review_scores_service(
        review_scores: Storage = Depends(get_current_storage(db='ugc_db', collection="review_scores")),
        reviews: Storage = Depends(get_current_storage(db='ugc_db', collection="reviews")),
) -> UserReviewScoresService:
    return UserReviewScoresService(ReviewScore, review_scores, reviews)
