import logging

import uvicorn
from aiokafka.helpers import create_ssl_context
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from aiokafka import AIOKafkaProducer
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.v1 import movies_api
from core import config
from core.logger import LOGGING
from db import event_storage


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


sentry_sdk.init(dsn=config.SENTRY_DSN)


@app.on_event("startup")
async def startup():
    context = create_ssl_context(
        cafile=config.KAFKA_SSL_CAFILE,
    )
    producer = AIOKafkaProducer(
            bootstrap_servers=config.KAFKA_SERVERS,
            security_protocol=config.KAFKA_SECURITY_PROTOCOL,
            sasl_mechanism=config.KAFKA_SASL_MECHANISM,
            sasl_plain_password=config.KAFKA_SASL_PLAIN_PASSWORD,
            sasl_plain_username=config.KAFKA_SASL_PLAIN_USERNAME,
            ssl_context=context
    )
    event_storage.storage = event_storage.KafkaStorage(producer)


app.include_router(movies_api.router, prefix="/v1/movies", tags=["Movies"])


@app.on_event("shutdown")
async def shutdown():
    event_storage.storage.close()

app = SentryAsgiMiddleware(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
