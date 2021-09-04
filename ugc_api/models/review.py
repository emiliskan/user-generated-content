from datetime import datetime
from typing import List, Optional
from uuid import UUID

from models.base import AbstractModel, BaseQuery
from pydantic import Field


class Review(AbstractModel):
    user_id: Optional[UUID]
    movie_id: UUID
    text: str = Field(max_length=1000)
    pub_date: datetime = datetime.now()
    rating: float = 0
    scores: List[UUID] = []


class ReviewQuery(BaseQuery):
    ...
