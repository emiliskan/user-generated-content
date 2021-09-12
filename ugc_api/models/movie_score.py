from uuid import UUID
from models.base import AbstractModel, FastJSONModel


class MovieScore(AbstractModel):
    user_id: UUID
    movie_id: UUID
    score: int


class MovieScoreQuery(FastJSONModel):
    movie_id: UUID
    score: int
