from datetime import datetime
from typing import List
from uuid import UUID

from models.base import AbstractModel
from pydantic import Field


class Review(AbstractModel):
    user_id: UUID
    movie_id: UUID
    pub_date: datetime
    text: str = Field(max_length=1000)
    movie_score_id: UUID
    rating: int
    scores: List[UUID]
    scores_quality: int
