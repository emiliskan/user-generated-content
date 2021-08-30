from typing import ClassVar
from db import Storage


class BaseService:
    def __init__(self, model: ClassVar, storage: Storage):
        self.model = model
        self.storage = storage
