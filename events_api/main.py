import logging

import uvicorn as uvicorn
from api.v1 import movies_api
from core import config
from core.logger import LOGGING
from db.kafka_producer import kafka_producer_client
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pass

app.include_router(movies_api.router, prefix="/v1/movies", tags=["Movies"])


@app.on_event("shutdown")
async def shutdown():
    await kafka_producer_client.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=LOGGING, log_level=logging.DEBUG, reload=True)
