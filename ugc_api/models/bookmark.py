from uuid import UUID
from models.base import AbstractModel


class BookMark(AbstractModel):
    user_id: UUID
    movie_id: UUID