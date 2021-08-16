import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
KAFKA_SERVERS = [f'{KAFKA_HOST}:{KAFKA_PORT}']

# AUTH
AUTH_HOST = os.getenv("AUTH_HOST", "localhost")
AUTH_PORT = os.getenv("AUTH_PORT", "5000")
AUTH_ENDPOINT = os.getenv("AUTH_ENDPOINT", "api/v1/user")
AUTH_URL = f"http://{AUTH_HOST}:{AUTH_PORT}/{AUTH_ENDPOINT}"
AUTH_BACKOFF_TIME = int(os.getenv("AUTH_BACKOFF_TIME", 10))

BACKOFF_FACTOR = float(os.getenv("BACKOFF_FACTOR", 0.5))
