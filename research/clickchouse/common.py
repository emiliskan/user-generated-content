import datetime
import random
import uuid
from typing import Iterator

FAKE_USER_IDS = [uuid.uuid4() for _ in range(1)]
FAKE_MOVIE_IDS = [uuid.uuid4() for _ in range(1)]
MAX_MOVIE_DURATION = 360


def generate_row() -> dict:
    return {
        'user_id': random.choice(FAKE_USER_IDS),
        'movie_id': random.choice(FAKE_MOVIE_IDS),
        'viewed_frame': random.randint(1, MAX_MOVIE_DURATION),
        'event_time': datetime.datetime.now(),
    }


def generate_batch(size: int) -> list[dict]:
    return [generate_row() for _ in range(size)]


def generate_fake_data(size: int, count: int) -> Iterator:
    return (generate_batch(size) for _ in range(count))
