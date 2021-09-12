import logging
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.security import HTTPBearer

from models import MovieScore, MovieScoreQuery
from services import MovieScoresService, get_movie_scores_service
from core.auth import auth

router = APIRouter()
logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer()


@router.post("/scores/movie_score", status_code=201)
async def create_movie_score(
        movie_score: MovieScoreQuery,
        service: MovieScoresService = Depends(get_movie_scores_service),
        user_id: str = Depends(auth),
) -> MovieScore:

    result = await service.add(user_id, movie_score.dict())
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Could not add movie score")

    return result


@router.get("/scores/movie_score/{movie_id}",
            response_model=MovieScore)
async def get_movie_score(
        movie_id: UUID = Query(None),
        service: MovieScoresService = Depends(get_movie_scores_service),
        user_id: str = Depends(auth),
) -> MovieScore:

    result = await service.get(user_id, movie_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Movie score not exists")
    return result


@router.delete("/scores/movie_score/{movie_id}")
async def delete_movie_score(
        movie_id: UUID = Query(None),
        service: MovieScoresService = Depends(get_movie_scores_service),
        user_id: str = Depends(auth),
) -> None:
    if not await service.remove(user_id, movie_id):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Could not remove movie score")


@router.patch("/scores/movie_score",
              response_model=MovieScore)
async def update_movie_score(
        movie_score: MovieScoreQuery,
        service: MovieScoresService = Depends(get_movie_scores_service),
        user_id: str = Depends(auth),
) -> MovieScore:

    result = await service.update(user_id, movie_score.dict())
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Could not update movie score")

    return result
