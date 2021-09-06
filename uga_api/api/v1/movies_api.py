import logging


from fastapi import APIRouter, Depends

from services.movies import MoviesService, get_movies_service
from core.auth import auth

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/save_movie_progress",
            summary="Сохранить прогресс фильма пользователя",
            description="Добавляет в базу прогресс фильма по пользователю"
            )
async def save_movie_progress(
        movie_id: str,
        viewed_frame: str,
        user_id: str = Depends(auth),
        movie_service: MoviesService = Depends(get_movies_service),
) -> None:

    await movie_service.save_movie_progress(movie_id, user_id, viewed_frame)

