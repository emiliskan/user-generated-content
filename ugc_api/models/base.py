from typing import List
from uuid import uuid4, UUID

import orjson
from bson import ObjectId as BsonObjectId

from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class AbstractModel(BaseModel):
    id: PydanticObjectId = Field(alias='id', default=PydanticObjectId())

    class Config:
        arbitrary_types_allowed = True

    class Meta:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseQuery(AbstractModel):
    sort_fields: List[str]
