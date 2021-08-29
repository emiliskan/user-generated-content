import logging

from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/reviews/{movie_id}")
async def create_review():
    pass


@router.get("/reviews/{movie_id}")
async def get_review():
    pass


@router.delete("/reviews/{movie_id}")
async def delete_review():
    pass


@router.patch("/reviews/{movie_id}")
async def update_review():
    pass
