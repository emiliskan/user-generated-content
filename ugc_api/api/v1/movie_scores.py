import logging
from http import HTTPStatus

from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials

from models import MovieScore
from services import MovieScoresService, get_movie_scores_service
from services.auth import get_user_id

from services.auth import AuthServiceUnavailable

router = APIRouter()
logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer()


@router.post("/scores/movies",
             response_model=MovieScore,)
async def create_movie_score(
                service: MovieScoresService = Depends(get_movie_scores_service),
                credentials: HTTPBasicCredentials = Depends(auth_scheme)) -> None:

    try:
        user_id = await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    await service.add(user_id)


@router.get("/scores/movies/{movie_score_id}",
            response_model=MovieScore)
async def get_movie_score(
        movie_id: str = Query(None, description="Movie ID"),
        service: MovieScoresService = Depends(get_movie_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme)) -> None:
    try:
        await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    # FIXME us
    await service.get(movie_id)


@router.delete("/scores/movies/{movie_score_id}",
               response_model=MovieScore)
async def delete_movie_score(
        movie_core_id: str = Query(None, description="Movie score ID"),
        service: MovieScoresService = Depends(get_movie_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme)) -> None:
    try:
        await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    await service.remove(movie_core_id)


@router.patch("/scores/movies/{movie_score_id}",
              response_model=MovieScore)
async def update_movie_score(
        service: MovieScoresService = Depends(get_movie_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme)) -> None:
    try:
        user_id = await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    await service.add(user_id)
