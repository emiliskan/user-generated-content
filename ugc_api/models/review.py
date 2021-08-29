from models.base import AbstractModel


class Review(AbstractModel):
    title: str
    body: str
