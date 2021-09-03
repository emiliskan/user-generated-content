from typing import List
from uuid import UUID

from models.base import AbstractModel


class UserBookmarks(AbstractModel):
    bookmarks: List[UUID]
