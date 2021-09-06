import logging
from http import HTTPStatus
from bson import ObjectId

from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials

from models import MovieScore, CreateMovieScore, UpdateMovieScore, PydanticObjectId
from services import MovieScoresService, get_movie_scores_service
from services.auth import get_user_id

from services.auth import AuthServiceUnavailable

router = APIRouter()
logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer()


@router.post("/scores/movie_score", status_code=201)
async def create_movie_score(
        movie_score: CreateMovieScore,
        service: MovieScoresService = Depends(get_movie_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme),
) -> MovieScore:

    try:
        user_id = await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    result = await service.add(user_id, movie_score.dict())
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Could not add movie score")

    return result


@router.get("/scores/movie_score/{movie_score_id}",
            response_model=MovieScore)
async def get_movie_score(
        movie_score_id: str = Query(None),
        service: MovieScoresService = Depends(get_movie_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme)
) -> MovieScore:
    try:
        await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    movie_id = PydanticObjectId(movie_score_id)
    result = await service.get(movie_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Movie score not exists")

    return result


@router.delete("/scores/movie_score/{movie_score_id}")
async def delete_movie_score(
        movie_score_id: str = Query(None),
        service: MovieScoresService = Depends(get_movie_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme)) -> None:
    try:
        await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    movie_core_id = ObjectId(movie_score_id)
    if not await service.remove(movie_core_id):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Could not remove movie score")


@router.patch("/scores/movie_score",
              response_model=MovieScore)
async def update_movie_score(
        movie_score: UpdateMovieScore,
        service: MovieScoresService = Depends(get_movie_scores_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme)) -> MovieScore:
    try:
        user_id = await get_user_id(credentials.credentials)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    result = await service.update(user_id, movie_score.dict())
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Could not update movie score")

    return result
