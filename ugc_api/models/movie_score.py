from models.base import AbstractModel


class MovieScore(AbstractModel):
    user_id: str  # TODO add validation for UUID
    movie_id: str
    score: int