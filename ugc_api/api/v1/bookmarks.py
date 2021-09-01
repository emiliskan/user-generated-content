import logging

from fastapi import APIRouter, Query, Depends, Header
from fastapi.security import HTTPBearer, HTTPBasicCredentials

from models import UserBookmarks
from services.bookmarks import UserBookmarksService, get_user_bookmarks_service
from services.auth import get_user_id

router = APIRouter()
logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer()


@router.post("/bookmarks/{movie_id}",
             description="Add movie to user's bookmarks")
async def create_bookmark(
        movie_id: str = Query(None, description="Movie ID"),
        service: UserBookmarksService = Depends(get_user_bookmarks_service),
        credentials: HTTPBasicCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    user_id = await get_user_id(token)
    await service.add(user_id, movie_id)


@router.get("/bookmarks",
            response_model=UserBookmarks,
            description="Get all user's bookmarks")
async def get_bookmark(service: UserBookmarksService = Depends(get_user_bookmarks_service),
                       credentials: HTTPBasicCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    user_id = await get_user_id(token)
    bookmarks = await service.get(user_id)
    return bookmarks


@router.delete("/bookmarks/{movie_id}",
               description="Remove movie from user's bookmarks")
async def delete_bookmark(
        movie_id: str = Query(None, description="Movie ID"),
        service: UserBookmarksService = Depends(get_user_bookmarks_service)
):
    user_id = ""
    await service.remove(user_id, movie_id)

