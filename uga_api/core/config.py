import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

KAFKA_HOST = os.getenv("KAFKA_HOST", "rc1a-mi7khra801ifkpfs.mdb.yandexcloud.net")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9091")
KAFKA_SERVERS = [f'{KAFKA_HOST}:{KAFKA_PORT}']
KAFKA_SECURITY_PROTOCOL = "SASL_SSL"
KAFKA_SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM", "SCRAM-SHA-512")
KAFKA_SASL_PLAIN_PASSWORD = os.getenv("KAFKA_SASL_PLAIN_PASSWORD", "aaaaaaaa")
KAFKA_SASL_PLAIN_USERNAME = os.getenv("KAFKA_SASL_PLAIN_USERNAME", "uga_api")
KAFKA_SSL_CAFILE = os.getenv("KAFKA_SSL_CAFILE", "$HOME/.kafka/CA.crt")

# AUTH
AUTH_HOST = os.getenv("AUTH_HOST", "localhost")
AUTH_PORT = os.getenv("AUTH_PORT", "5000")
AUTH_ENDPOINT = os.getenv("AUTH_ENDPOINT", "api/v1/user")
AUTH_URL = f"http://{AUTH_HOST}:{AUTH_PORT}/{AUTH_ENDPOINT}"
AUTH_BACKOFF_TIME = int(os.getenv("AUTH_BACKOFF_TIME", 10))

BACKOFF_FACTOR = float(os.getenv("BACKOFF_FACTOR", 0.5))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
