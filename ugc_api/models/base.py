from uuid import uuid4, UUID

import orjson
from bson import ObjectId

from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class AbstractModel(BaseModel):
    id: UUID = Field(alias='_id', default=uuid4())

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    class Meta:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps