import random

from pymongo import MongoClient, DESCENDING

from config import (MONGO_PORT, MONGO_HOST, DB_NAME,
                    BENCHMARK_ITERATIONS, MAX_RATING, MIN_RATING)
from misc import (benchmark, get_id, get_random_field,
                  get_random_date, inc_avg_mean)

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.get_database(DB_NAME)


USER_BOOKMARKS = db.get_collection("user_bookmarks")
MOVIES = db.get_collection("movies")
MOVIE_SCORES = db.get_collection("movie_scores")
REVIEWS = db.get_collection("reviews")
REVIEW_SCORES = db.get_collection("review_scores")

USER_ID = get_random_field(db, "user_bookmarks")
MOVIE_ID = get_random_field(db, "movies")
REVIEW_ID = get_random_field(db, "reviews")


@benchmark(BENCHMARK_ITERATIONS)
def get_user_benchmarks():
    query = {"_id": USER_ID}
    user = USER_BOOKMARKS.find(query)[0]
    return len(user.get("bookmarks"))


@benchmark(BENCHMARK_ITERATIONS)
def get_movie_reviews_sort_pub_date():
    query = {"movie_id": MOVIE_ID}
    return len(list(REVIEWS.find(query).sort("pub_date", DESCENDING)))


@benchmark(BENCHMARK_ITERATIONS)
def get_movie_reviews_sort_scores_quality():
    query = {"movie_id": MOVIE_ID}
    reviews = REVIEWS.find(query).sort("scores_quality", DESCENDING)
    return len(list(reviews))


@benchmark(BENCHMARK_ITERATIONS)
def get_user_liked_movies():
    query = {"user_id": USER_ID, "score": {"$gte": 5}}
    good_ratings = MOVIE_SCORES.find(query)
    return len([rating.get("movie_id") for rating in good_ratings])


@benchmark(BENCHMARK_ITERATIONS)
def get_user_liked_reviews():
    query = {"user_id": USER_ID, "score": {"$gte": 5}}
    good_ratings = REVIEW_SCORES.find(query)
    return len([rating.get("review_id") for rating in good_ratings])


@benchmark(BENCHMARK_ITERATIONS)
def get_movie_scores_quality():
    query = {"_id": MOVIE_ID}
    movie = MOVIES.find_one(query)
    return movie.get("scores_quality")


@benchmark(BENCHMARK_ITERATIONS)
def get_movie_good_ratings_count():
    query = {"movie_id": MOVIE_ID, "score": {'$gte': 5}}
    cnt = MOVIE_SCORES.count_documents(query)
    return cnt


@benchmark(BENCHMARK_ITERATIONS)
def add_movie_score():
    value = random.randint(MIN_RATING, MAX_RATING)
    score_id = get_id()
    score = {
        "_id": score_id,
        "user_id": USER_ID,
        "movie_id": MOVIE_ID,
        "score": value,
    }

    MOVIE_SCORES.insert_one(score)

    movie = MOVIES.find_one({"_id": MOVIE_ID})
    old_rating = movie.get("rating")
    scores_quality = movie.get("scores_quality")
    new_rating = inc_avg_mean(old_rating, scores_quality, value)

    MOVIES.update(
        {"_id": MOVIE_ID},
        {
            "$addToSet": {"scores": score_id},
            "$inc": {"scores_quality": 1},
            "$set": {"rating": new_rating}
         }
    )

    return f"Add movie score"


@benchmark(BENCHMARK_ITERATIONS)
def add_review_score():
    value = random.randint(MIN_RATING, MAX_RATING)
    score_id = get_id()
    score = {
        "_id": score_id,
        "user_id": USER_ID,
        "review_id": REVIEW_ID,
        "score": value,
    }

    REVIEW_SCORES.insert_one(score)

    review = REVIEWS.find_one({"_id": REVIEW_ID})
    old_rating = review.get("rating")
    scores_quality = review.get("scores_quality")
    new_rating = inc_avg_mean(old_rating, scores_quality, value)

    REVIEWS.update(
        {"_id": REVIEW_ID},
        {
            "$addToSet": {"scores": score_id},
            "$inc": {"scores_quality": 1},
            "$set": {"rating": new_rating}
        }
    )

    return f"Add review score"


@benchmark(BENCHMARK_ITERATIONS)
def add_bookmark():
    movie_id = get_id()
    USER_BOOKMARKS.update_one(
        {"_id": USER_ID},
        {"$addToSet": {"bookmarks": movie_id}}
    )
    return f"Added bookmark for movie: {movie_id} to user: {USER_ID}"


@benchmark(BENCHMARK_ITERATIONS)
def add_review():
    review_id = get_id()
    score_id = get_id()
    score_value = random.randint(MIN_RATING, MAX_RATING)
    score = {
        "_id": score_id,
        "user_id": USER_ID,
        "movie_id": MOVIE_ID,
        "score": score_value,
    }

    review = {
        "_id": review_id,
        "user_id": USER_ID,
        "movie_id": MOVIE_ID,
        "pub_date": get_random_date(),
        "text": f"Test review for {MOVIE_ID} by {USER_ID}",
        "movie_score_id": score_id,
        "rating": 0,
        "scores": 0,
        "scores_quality": 0,
    }

    MOVIE_SCORES.insert_one(score)

    movie = MOVIES.find_one({"_id": MOVIE_ID})
    old_rating = movie.get("rating")
    scores_quality = movie.get("scores_quality")
    new_rating = inc_avg_mean(old_rating, scores_quality, score_value)

    MOVIES.update(
        {"_id": MOVIE_ID},
        {
            "$addToSet": {"scores": score_id},
            "$inc": {"scores_quality": 1},
            "$set": {"rating": new_rating}
        }
    )
    REVIEWS.insert_one(review)
    return f'Added movie_review with id: {review_id}'


READ_TESTS = (
    get_user_benchmarks,
    get_movie_reviews_sort_pub_date,
    get_movie_reviews_sort_scores_quality,
    get_user_liked_movies,
    get_user_liked_reviews,
    get_movie_scores_quality,
    get_movie_good_ratings_count,
)

WRITE_TESTS = (
    add_bookmark,
    add_review,
    add_movie_score,
    add_review_score,
)