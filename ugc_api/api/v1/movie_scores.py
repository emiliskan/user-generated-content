import logging

from fastapi import APIRouter

from models.movie_score import MovieScore

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scores/movies",
             response_model=MovieScore)
async def create_movie_score():
    pass


@router.get("/scores/movies/{movie_score_id}",
            response_model=MovieScore)
async def get_movie_score():
    pass


@router.delete("/scores/movies/{movie_score_id}",
               response_model=MovieScore)
async def delete_movie_score():
    pass


@router.patch("/scores/movies/{movie_score_id}",
              response_model=MovieScore)
async def update_movie_score():
    pass
