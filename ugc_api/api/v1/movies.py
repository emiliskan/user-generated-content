import logging
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Query, Depends, HTTPException

from models import Movie
from services import MovieService, get_movie_service
from services.exceptions import DocumentNotFound

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/scores/movies/{movie_id}",
            response_model=Movie)
async def get_movie_score(
        movie_id: UUID = Query(None, description="Movie ID"),
        service: MovieService = Depends(get_movie_service)
) -> Movie:

    try:
        result = await service.get(movie_id)
    except DocumentNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Movie not exists")

    return result
