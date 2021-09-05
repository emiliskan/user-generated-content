import logging
from http import HTTPStatus

from fastapi import APIRouter, Query, Depends, HTTPException

from models import Movie
from services import MovieService, get_movie_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/scores/movies/{movie_id}",
            response_model=Movie)
async def get_movie_score(
        movie_id: str = Query(None, description="Movie ID"),
        service: MovieService = Depends(get_movie_service)
) -> Movie:
    print(movie_id)
    result = await service.get(movie_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Movie not exists")

    return result
