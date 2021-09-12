from functools import lru_cache
from typing import ClassVar
from uuid import UUID

from fastapi import Depends

from common import inc_avg_mean
from core.config import MONGO_DB
from db import Storage, get_current_storage
from models import MovieScore


def create_movie_info(movie_id: str) -> dict:
    return {
        "_id": movie_id,
        "rating": 0,
        "scores_quality": 0,
        "scores": [],
        "reviews": [],
    }


class MovieScoresService:
    def __init__(self, model: ClassVar, movies: Storage, scores: Storage):
        self.model = model
        self.movies = movies
        self.scores = scores

    async def get(self, user_id: str, movie_id: UUID):
        spec = {
            "user_id": user_id,
            "movie_id": movie_id
        }
        print(spec)
        result = await self.scores.get(spec)
        return result

    async def add(self, user_id: str,  movie_score: dict):
        movie_score["user_id"] = user_id
        spec = {"_id": movie_score["movie_id"]}
        movie = await self.movies.get(spec)

        if not movie:
            movie_info = create_movie_info(movie_score["movie_id"])
            movie = await self.movies.create(movie_info)

        result = await self.scores.create(movie_score)
        score_id = result.inserted_id

        new_rating = inc_avg_mean(movie["rating"],
                                  movie["scores_quality"],
                                  movie_score["score"])
        doc = {
                "$addToSet": {"scores": score_id},
                "$inc": {"scores_quality": 1},
                "$set": {"rating": new_rating}
        }

        if await self.movies.update(spec, doc):
            return self.model(**await self.scores.get({"_id": score_id}))

    async def remove(self, user_id: str, movie_id: UUID):
        spec = {
            "user_id": user_id,
            "movie_id": movie_id
        }
        movie_score = await self.scores.get(spec)
        if not movie_score:
            return None

        score_id = movie_score["_id"]
        movie_id = movie_score["movie_id"]

        await self.scores.delete({"_id": score_id})

        movie = await self.movies.get({"_id": movie_id})

        length = movie["scores_quality"]
        scores = await self.scores.search(
            filters={"movie_id": movie_score["movie_id"]},
            limit=length
        )
        new_rating = sum(s["score"] for s in scores) / length

        doc = {
            "$addToSet": {"scores": score_id},
            "$inc": {"scores_quality": -1},
            "$set": {"rating": new_rating}
        }
        return await self.movies.update({"_id": movie_id}, doc)

    async def update(self, user_id: str, movie_score: dict):
        spec = {
            "user_id": user_id,
            "movie_id": movie_score["movie_id"],
        }
        score = await self.scores.get(spec)
        if not score:
            return None

        score_id = score["_id"]
        doc = {"$set": {"score": movie_score["score"]}}
        if not await self.scores.update({"_id": score_id}, doc):
            return None

        movie = await self.movies.get({"_id": movie_score["movie_id"]})
        if not movie:
            return None

        length = movie["scores_quality"]
        scores = await self.scores.search(
            filters={"movie_id": movie_score["movie_id"]},
            limit=length
        )
        new_rating = sum(s["score"] for s in scores) / length

        doc = {"$set": {"rating": new_rating}}
        if await self.movies.update({"_id": movie_score["movie_id"]}, doc):
            return await self.scores.get({"_id": score_id})


@lru_cache()
def get_movie_scores_service(
        movies: Storage = Depends(get_current_storage(
            db=MONGO_DB, collection="movies")),
        scores: Storage = Depends(get_current_storage(
            db=MONGO_DB, collection="movie_scores")),
) -> MovieScoresService:
    return MovieScoresService(MovieScore, movies, scores)
