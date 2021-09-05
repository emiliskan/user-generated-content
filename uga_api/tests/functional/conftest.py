from dataclasses import dataclass

import pytest
import aiohttp
import asyncio

from multidict import CIMultiDictProxy

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


@pytest.fixture
async def auth(make_post_request) -> str:
    """
    Authorize user in auth service
    :param make_post_request:
    :return: Access token
    """
    data = {
        "username": "test_user",
        "password": "asJDjDahJKjdHsd",
        "email": "test_user@yandex.ru"
    }
    url = f"{settings.AUTH_SERVICE_URL}/api/v1/user"
    # Temporary return default token to test
    return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzMDg2NTg2MCwianRpIjoiMmM0YTY3MDYtOGJkNy00ZGY0LWFmMjEtMjg5NjI3YTBmNmQ2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijc3MDc2MDljLWNkNTctNDJlYy04MzhiLTNlN2UxOWMxYTljOSIsIm5iZiI6MTYzMDg2NTg2MCwiZXhwIjoxNjMwODY5NDYwLCJyb2xlIjpudWxsLCJzZXNzaW9uIjoiMjkxMDZhYzUtOGE3YS00YzJjLTg5ZjEtMDAzMjJlZWM5NThhIn0.Mq_b2cIBvMpVstprVHNI5Vd2YyL3SiOmkbu5PWLezCg"


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
        async with session.post(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
