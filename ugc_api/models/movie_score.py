from uuid import UUID

from models.base import AbstractModel


class MovieScore(AbstractModel):
    user_id: UUID  # TODO add validation for UUID
    movie_id: UUID
    score: int