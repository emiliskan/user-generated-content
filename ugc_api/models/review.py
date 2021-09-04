from datetime import datetime
from typing import List
from uuid import UUID

from models.base import AbstractModel, BaseQuery
from pydantic import Field


class Review(AbstractModel):
    movie_id: UUID
    text: str = Field(max_length=1000)
    pub_date: datetime = datetime.now()
    rating: int = 0
    scores: List[UUID] = []
    scores_quality: int = 0


class ReviewAnswer(Review):
    user_id: UUID


class ReviewQuery(BaseQuery):
    filters: dict
    offset: int
    limit: int
