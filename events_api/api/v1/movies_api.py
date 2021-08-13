import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Header

from services.movies import MoviesService, get_movies_service
from utils.auth import get_user_info, UserNotFound, AuthServiceUnavailable, ServerError, AuthTokenRequired

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

    token = Authorization.replace("Bearer ", "")
    try:
        user_info = await get_user_info(token)
    except AuthTokenRequired:
        raise HTTPException(status_code=HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED)
    except ServerError:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    except AuthServiceUnavailable:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)
    except UserNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    await movie_service.save_movie_progress(movie_id, user_info["id"], viewed_frame)

