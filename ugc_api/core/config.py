import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv("PROJECT_NAME", "ugc")

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "ugc_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "movies")
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "")
MONGO_SSL_CA = os.getenv("MONGO_SSL_CA", "")

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?replicaSet=rs01&authSource={MONGO_DB}"

BACKOFF_FACTOR = float(os.getenv('BACKOFF_FACTOR', 0.5))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("Not found JWT_SECRET_KEY")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# LOGGING
SENTRY_DSN = os.getenv('SENTRY_DSN', 'https://985de561392e4d6391fb209958b7eda5@o977346.ingest.sentry.io/5933885')
LOGSTASH_PORT = 5044
