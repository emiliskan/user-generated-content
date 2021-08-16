import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from kafka import KafkaProducer

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


@app.on_event("startup")
async def startup():
    event_storage.storage = event_storage.KafkaStorage(
        KafkaProducer(
            bootstrap_servers=config.KAFKA_SERVERS,
            security_protocol="SASL_SSL",
            sasl_mechanism=config.KAFKA_SASL_MECHANISM,
            sasl_plain_password=config.KAFKA_SASL_PLAIN_PASSWORD,
            sasl_plain_username=config.KAFKA_SASL_PLAIN_USERNAME,
            ssl_cafile=config.KAFKA_SSL_CAFILE
        )
    )

app.include_router(movies_api.router, prefix="/v1/movies", tags=["Movies"])


@app.on_event("shutdown")
async def shutdown():
    event_storage.storage.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
