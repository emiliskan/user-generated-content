import json

from pydantic import BaseModel


def get_object_to_es(index: str, obj: BaseModel) -> list[str]:
    return [
        json.dumps({"update": {"_index": index, "_id": obj.id}}),
        json.dumps({"doc": obj.dict(), "doc_as_upsert": True}),
    ]
