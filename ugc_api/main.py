import logging
import ssl

import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.v1 import movie_scores, review_scores, bookmarks, reviews, movies
from core import config
from core.logger import LOGGING
from db.storage import connect_db, close_db

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

sentry_sdk.init(dsn=config.SENTRY_DSN)


@app.on_event("startup")
async def startup():
    await connect_db(
        host=config.MONGO_HOST,
        port=config.MONGO_PORT,
        ssl_ca_certs=config.MONGO_SSL_CA,
        user=config.MONGO_USER,
        password=config.MONGO_PASS,
    )


@app.on_event("shutdown")
async def shutdown():
    await close_db()


app.include_router(bookmarks.router, prefix="/api/v1", tags=["Bookmarks"])
app.include_router(reviews.router, prefix="/api/v1", tags=["Reviews"])
app.include_router(review_scores.router, prefix="/api/v1", tags=["ReviewScores"])
app.include_router(movies.router, prefix="/api/v1", tags=["Movies"])
app.include_router(movie_scores.router, prefix="/api/v1", tags=["MovieScores"])

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
