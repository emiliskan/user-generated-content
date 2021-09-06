from uuid import UUID
from pydantic import BaseModel
from models.base import AbstractModel, FastJSONModel, PydanticObjectId


class MovieScore(AbstractModel):
    user_id: UUID
    movie_id: UUID
    score: int


class CreateMovieScore(FastJSONModel):
    movie_id: UUID
    score: int


class UpdateMovieScore(BaseModel):
    id:  PydanticObjectId
    movie_id: UUID
    score: int
