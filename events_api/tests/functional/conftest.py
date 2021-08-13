import asyncio
import json
import os
from dataclasses import dataclass

import aiohttp
import aioredis
import backoff
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ElasticsearchException
from fastapi import status
from multidict import CIMultiDictProxy

from models.film import Film
from models.person import Person
from models.genre import Genre

from tests.functional.settings import TestSettings
from tests.functional.utils.utils import get_object_to_es

test_settings = TestSettings()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> TestSettings:
    return TestSettings()


@backoff.on_exception(backoff.expo, ElasticsearchException, max_tries=20)
@pytest.fixture(scope="session")
async def es_client(settings):
    client = AsyncElasticsearch(hosts=f"{settings.es_host}:{settings.es_port}")
    yield client
    await client.close()


@pytest.fixture
async def redis_client(settings):
    client = await aioredis.create_redis_pool((settings.redis_host, settings.redis_port))
    yield client
    client.close()
    await client.wait_closed()


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60)
@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session, settings):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"http://{settings.backend_api_host}:{settings.backend_api_port}/v1/{method}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(
    autouse=True,
    scope="session",
    params=[
        (
            "movies",
            os.path.join(test_settings.test_data_dir, "movies_index.json"),
            os.path.join(test_settings.test_data_dir, "movies_data.json"),
            Film,
        ),
        (
            "persons",
            os.path.join(test_settings.test_data_dir, "persons_index.json"),
            os.path.join(test_settings.test_data_dir, "persons_data.json"),
            Person,
        ),
        (
            "genres",
            os.path.join(test_settings.test_data_dir, "genres_index.json"),
            os.path.join(test_settings.test_data_dir, "genres_data.json"),
            Genre,
        ),
    ],
)
async def data_to_es(es_client, request):
    index, es_index, es_data, pydantic_model = request.param

    # Create index.
    with open(es_index) as file:
        body: dict = json.load(file)
        await es_client.indices.create(index=index, body=body, ignore=[status.HTTP_400_BAD_REQUEST])

    # Extract.
    with open(es_data) as file:
        objs: list = json.load(file)
        objs = [pydantic_model.parse_obj(obj) for obj in objs]

    # Transform.
    objs_to_es: list = []
    for obj in objs:
        objs_to_es.extend(get_object_to_es(index, obj))
    prepare_data: str = "\n".join(objs_to_es) + "\n"

    # Load.
    await es_client.bulk(index=index, body=prepare_data)
