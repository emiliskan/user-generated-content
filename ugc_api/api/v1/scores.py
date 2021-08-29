import logging

from fastapi import APIRouter

from models.score import Score

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scores/{movie_id}",
             response_model=Score)
async def create_score():
    pass


@router.get("/scores/{movie_id}",
            response_model=Score)
async def get_():
    pass


@router.delete("/scores/{movie_id}",
               response_model=Score)
async def delete_mark():
    pass


@router.patch("/scores/{movie_id}",
              response_model=Score)
async def update_mark():
    pass
