from uuid import uuid4, UUID

import orjson
from bson import ObjectId

from pydantic import BaseModel, Field
from bson import ObjectId as BsonObjectId


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class FastJSONModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    class Meta:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, BsonObjectId):
            return str(v)
        elif isinstance(v, str):
            return BsonObjectId(v)


class AbstractModel(BaseModel):
    id: PydanticObjectId = Field(alias="_id", default=uuid4())
