from typing import Optional
from uuid import UUID

from models.base import AbstractModel, PydanticObjectId


class ReviewScore(AbstractModel):
    review_id: PydanticObjectId
    user_id: Optional[UUID]
    score: int
