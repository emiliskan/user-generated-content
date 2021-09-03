import json
import uuid

import aiohttp
import backoff
from aiohttp import ClientConnectionError
from core.config import AUTH_BACKOFF_TIME, AUTH_URL, BACKOFF_FACTOR


class AuthServiceUnavailable(BaseException):
    ...


class UserNotFound(BaseException):
    ...


def giveup_handler(details):
    raise AuthServiceUnavailable


@backoff.on_exception(backoff.expo,
                      ClientConnectionError,
                      max_time=AUTH_BACKOFF_TIME,
                      factor=BACKOFF_FACTOR,
                      on_giveup=giveup_handler)
async def get_user_id(token: str) -> str:
    async with aiohttp.ClientSession() as session:
        token = f"Bearer {token}"
        headers = {"Authorization": token}

        async with session.get(AUTH_URL, headers=headers) as response:
            if response.status == 200:
                response_body = await response.text()
                return json.loads(response_body)["id"]
            elif response.status == 404:
                raise UserNotFound
            else:
                raise AuthServiceUnavailable