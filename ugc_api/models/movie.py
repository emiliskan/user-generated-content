from datetime import datetime
from typing import List

from models.base import AbstractModel
from pydantic import Field


class Review(AbstractModel):
    rating: int
    scores: List[str]
    scores_quality: int
    reviews: List[str]
