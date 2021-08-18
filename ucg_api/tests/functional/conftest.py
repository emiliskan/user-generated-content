from dataclasses import dataclass

import pytest
import aiohttp
import asyncio

from aiokafka.helpers import create_ssl_context
from multidict import CIMultiDictProxy
from aiokafka import AIOKafkaConsumer

import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def kafka_consumer():
    context = create_ssl_context(
        cafile=settings.KAFKA_SSL_CAFILE,
    )
    client = AIOKafkaConsumer(
            bootstrap_servers=settings.KAFKA_SERVERS,
            security_protocol=settings.KAFKA_SECURITY_PROTOCOL,
            sasl_mechanism=settings.KAFKA_SASL_MECHANISM,
            sasl_plain_password=settings.KAFKA_SASL_PLAIN_PASSWORD,
            sasl_plain_username=settings.KAFKA_SASL_PLAIN_USERNAME,
            ssl_context=context
    )
    yield client
    await client.stop()


@pytest.fixture
def auth(make_post_request):
    async def inner():
        url = f"{settings.AUTH_SERVICE_URL}/api/v1/auth"
        data = {
          "username": "alex2",
          "password": "password"
        }
        response = await make_post_request(url, data)
        assert response.status == 200, "something wrong with auth service."
        return response.body["accessToken"]
    return inner


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None, headers: dict = None) -> HTTPResponse:
        url = f"http://{settings.API_SERVICE_URL}/{settings.API}/{method}"
        async with session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_post_request(session):
    async def inner(url: str, data: dict = None, headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.post(url, data=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner