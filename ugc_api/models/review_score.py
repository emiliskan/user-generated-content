from models.base import AbstractModel


class ReviewScore(AbstractModel):
    review_id: str
    user_id: str
    score: int