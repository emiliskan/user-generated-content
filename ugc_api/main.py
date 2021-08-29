import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from api.v1 import scores, bookmarks, reviews
from core import config
from core.logger import LOGGING

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(bookmarks.router, prefix="/v1/user", tags=["Bookmarks"])
app.include_router(scores.router, prefix="/v1/user", tags=["Scores"])
app.include_router(reviews.router, prefix="/v1/user", tags=["Reviews"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
