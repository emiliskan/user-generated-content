import time

import asyncio
from dataclasses import dataclass

import aiohttp
import jwt
import pytest
from multidict import CIMultiDictProxy

from settings import (USER_ID, JWT_SECRET_KEY, JWT_ALGORITHM,
                      API_SERVICE_URL, API)


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
    playload = {
        "sub": USER_ID,
        "exp": time.time() + 100500
    }
    return jwt.encode(playload, JWT_SECRET_KEY, JWT_ALGORITHM)


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{API_SERVICE_URL}/{API}/{method}"
        async with session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_post_request(session):
    async def inner(url: str, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.post(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
