from models.base import AbstractModel


class User(AbstractModel):
    email: str
    username: str
