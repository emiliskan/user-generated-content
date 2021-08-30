from typing import Optional
from uuid import uuid4

import orjson
from bson import ObjectId

from pydantic import BaseModel, Field

from utils.pyobjectid import PyObjectId


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class AbstractModel(BaseModel):
    id: PyObjectId = Field(alias='_id', default=uuid4)  # TODO add validation for UUID

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    class Meta:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps