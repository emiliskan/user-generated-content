import logging

from fastapi import APIRouter

from models.review_score import ReviewScore

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scores/reviews/{movie_id}",
             response_model=ReviewScore)
async def create_review_score():
    pass


@router.get("/scores/reviews/{movie_id}",
            response_model=ReviewScore)
async def get_review_score():
    pass


@router.delete("/scores/reviews/{movie_id}",
               response_model=ReviewScore)
async def delete_review_score():
    pass


@router.patch("/scores/reviews/{movie_id}",
              response_model=ReviewScore)
async def update_review_score():
    pass
