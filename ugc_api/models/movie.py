from typing import List
from uuid import UUID, uuid4

from pydantic import Field

from models.base import FastJSONModel


class Movie(FastJSONModel):
    id: UUID = Field(alias="_id", default=uuid4())
    rating: float
    scores: List
    scores_quality: int
    reviews: List
