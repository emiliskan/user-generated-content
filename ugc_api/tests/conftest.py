import asyncio
import time
from dataclasses import dataclass

import aiohttp
import jwt
import pytest
from multidict import CIMultiDictProxy

from settings import USER_ID, JWT_SECRET_KEY, JWT_ALGORITHM


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
async def auth() -> str:
    payload = {
        "sub": USER_ID,
        "exp": time.time() + 100500
    }
    return jwt.encode(payload, JWT_SECRET_KEY, JWT_ALGORITHM)


@pytest.fixture
async def headers(auth) -> dict:
    return {"Authorization": f"Bearer {auth}"}


@pytest.fixture
def make_get_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.get(url, json=data, params=params,
                               headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_post_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.post(url, json=data, params=params,
                                headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_delete_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.delete(url, json=data, params=params,
                                  headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_patch_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.patch(url, json=data, params=params,
                                 headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
