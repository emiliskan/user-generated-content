from uuid import UUID

from models.base import AbstractModel


class ReviewScore(AbstractModel):
    review_id: UUID
    user_id: UUID
    score: int