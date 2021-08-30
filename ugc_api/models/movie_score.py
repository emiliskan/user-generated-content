from uuid import UUID

from models.base import AbstractModel


class MovieScore(AbstractModel):
    user_id: UUID
    movie_id: UUID
    score: int