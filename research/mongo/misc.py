import datetime
import uuid
import random

from typing import List, Tuple

from config import *


def get_id() -> str:
    return str(uuid.uuid4())


def get_random_date():
    start = datetime.datetime.strptime("1/1/2008 1:30 PM", "%m/%d/%Y %I:%M %p")
    delta = datetime.datetime.now() - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


USER_IDS = [get_id() for _ in range(USERS_COUNT)]
MOVIE_IDS = [get_id() for _ in range(MOVIES_COUNT)]


def generate_user_bookmarks():
    for uid in USER_IDS:
        yield {
            "_id": uid,
            "bookmarks": [
                mid for mid in random.sample(MOVIE_IDS, BOOKMARKS_PER_USER)
            ]
        }


def generate_movie_score(uid: str, mid: str) -> dict:
    score = {
        "_id": get_id(),
        "user_id": uid,
        "movie_id": mid,
        "score": random.randint(MIN_RATING, MAX_RATING),
    }
    return score


def generate_review_score(review_id: str) -> dict:
    score = {
        "_id": get_id(),
        "review_id": review_id,
        "user_id": random.choice(USER_IDS),
        "score": random.randint(MIN_RATING, MAX_RATING),
    }
    return score


def generated_single_review(user_id: str, movie_id: str,
                            movie_score_id: str) -> Tuple[dict, list]:
    review_id = get_id()
    scores_quality = random.randint(1, MAX_REVIEW_SCORE)
    scores = [generate_review_score(review_id) for _ in range(scores_quality)]
    rating = sum((s.get("score") for s in scores)) / scores_quality
    review = {
        "_id": get_id(),
        "user_id": user_id,
        "movie_id": movie_id,
        "pub_date": get_random_date(),
        "text": "Review text",
        "movie_score_id": movie_score_id,
        "rating": rating,
        "scores": [s.get("_id") for s in scores],
        "scores_quality": scores_quality,
    }
    return review, scores


def generated_movie(movie_id: str, scores: List[dict],
                    reviews: List[dict]) -> dict:
    scores_quality = len(scores)
    rating = sum((s.get("score") for s in scores)) / scores_quality
    movie = {
        "_id": movie_id,
        "rating": rating,
        "scores_quality": scores_quality,
        "scores": [s.get("_id") for s in scores],
        "reviews": [r.get("_id") for r in reviews]
    }
    return movie


def generate_movie_and_reviews(movie_id: str) -> Tuple[dict, list, list, list]:
    users_ids = random.sample(USER_IDS, MOVIES_PER_USER)

    movie_scores = []
    reviews = []
    reviews_scores = []

    for user_id in users_ids:
        ms = generate_movie_score(user_id, movie_id)
        movie_scores.append(ms)
        review, rs = generated_single_review(user_id, movie_id, ms.get("_id"))
        reviews.append(review)
        reviews_scores.extend(rs)

    movie = generated_movie(movie_id, movie_scores, reviews)

    return movie, movie_scores, reviews, reviews_scores


def upload_users_bookmarks(db):
    print("Starting upload user bookmarks")
    collection = db.get_collection("user_bookmarks")
    collection.insert_many(generate_user_bookmarks(), ordered=False)
    print("Done!")


def upload_movies_and_reviews(db):
    print("Starting upload movies and reviews")

    movies_coll = db.get_collection("movies")
    movies_score_coll = db.get_collection("movie_scores")
    reviews_coll = db.get_collection("reviews")
    reviews_score_coll = db.get_collection("review_scores")

    for idx, movie_id, in enumerate(MOVIE_IDS):
        movie, mss, reviews, rss = generate_movie_and_reviews(movie_id)
        movies_coll.insert_one(movie)
        movies_score_coll.insert_many(mss, ordered=False)
        reviews_coll.insert_many(reviews, ordered=False)
        reviews_score_coll.insert_many(rss, ordered=False)

        if idx % 100 == 0:
            print(f"load movies: {idx}")

    print("Done!")
