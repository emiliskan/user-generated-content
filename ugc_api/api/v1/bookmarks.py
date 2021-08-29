import logging
from typing import List
from fastapi import APIRouter, Query, Depends
from fastapi.security import HTTPBearer

from models.bookmark import BookMark

router = APIRouter()
logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer()


@router.post("/bookmarks/{movie_id}",
             response_model=BookMark,
             description="Add movie to bookmarks")
async def create_bookmark(movie_id: str = Query(None, description="Movie ID"),
                          token: str = Depends(auth_scheme)):
    pass


@router.get("/bookmarks",
            response_model=BookMark,
            description="Get all user's bookmarks")
async def get_bookmark() -> List[BookMark]:
    pass


@router.delete("/bookmarks/{movie_id}",
               response_model=BookMark,
               description="Remove movie from bookmarks")
async def delete_bookmark(movie_id: str = Query(None, description="Movie ID")):
    pass
