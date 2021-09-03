from functools import lru_cache
from typing import ClassVar

from fastapi import Depends
from db import Storage, get_current_storage
from models import MovieScore
from common import inc_avg_mean, reduce_avg_mean


class MovieScoresService:
    def __init__(self, model: ClassVar, movies: Storage, scores: Storage):
        self.model = model
        self.movies = movies
        self.scores = scores

    async def add(self, movie_score: dict):
        spec = {"_id": movie_score["_id"]}
        movie = await self.movies.get(spec)
        creat_move()
        score_id = await self.scores.create(movie_score)

        new_rating = inc_avg_mean(movie["rating"], movie["scores_quality"], movie_score["score"])
        doc = {
                "$addToSet": {"scores": score_id},
                "$inc": {"scores_quality": 1},
                "$set": {"rating": new_rating}
        }
        await self.movies.update(spec, doc)

    async def remove(self, score_id: str):
        movie_score = await self.scores.get({"_id": score_id})
        movie_id = movie_score["movie_id"]

        await self.scores.delete({"_id": score_id})

        movie = await self.movies.get({"_id": movie_id})

        new_rating = reduce_avg_mean(movie["rating"], movie["scores_quality"], movie_score["score"])
        doc = {
            "$addToSet": {"scores": score_id},
            "$inc": {"scores_quality": -1},
            "$set": {"rating": new_rating}
        }
        await self.movies.update({"_id": movie_id}, doc)

    async def get(self, movie_id):
        return await self.movies.get({"_id": movie_id})


@lru_cache()
def get_movie_scores_service(
        movies: Storage = Depends(get_current_storage(db='ugc_db', collection="movies")),
        scores: Storage = Depends(get_current_storage(db='ugc_db', collection="movies_score")),
) -> MovieScoresService:
    return MovieScoresService(MovieScore, movies, scores)
