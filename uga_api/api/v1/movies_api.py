import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Header

from services.movies import MoviesService, get_movies_service
from utils.auth import get_user_info, UserNotFound, AuthServiceUnavailable

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/save_movie_progress",
            summary="Сохранить прогресс фильма пользователя",
            description="Добавляет в базу прогресс фильма по пользователю"
            )
async def save_movie_progress(
        movie_id: str,
        viewed_frame: str,
        Authorization: str = Header(None),
        movie_service: MoviesService = Depends(get_movies_service),
) -> None:

    if Authorization is None:
        raise HTTPException(status_code=HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED, detail="Auth token required.")
    # temporary remove connecting to Auth
    '''try:
        user_info = await get_user_info(Authorization)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)
    except UserNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    await movie_service.save_movie_progress(movie_id, user_info.id, viewed_frame)'''
    await movie_service.save_movie_progress(movie_id, "87453e9b-e9d6-4caa-bbe2-9ffda193a999", viewed_frame)

