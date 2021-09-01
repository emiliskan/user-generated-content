import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from api.v1 import movie_scores, review_scores, bookmarks, reviews
from core import config
from core.logger import LOGGING
from db.storage import close_db

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(bookmarks.router, prefix="/api/v1", tags=["Bookmarks"])
app.include_router(review_scores.router, prefix="/api/v1", tags=["ReviewScores"])
app.include_router(movie_scores.router, prefix="/api/v1", tags=["MovieScores"])
app.include_router(reviews.router, prefix="/api/v1", tags=["Reviews"])

app.add_event_handler("shutdown", close_db)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
