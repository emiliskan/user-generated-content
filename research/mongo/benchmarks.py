#!/usr/bin/env python3
"""
Running read benchmarks for MongoDB...
Test name: get_user_benchmarks
Test iterations: 10
Full time: 0.017959600023459643 s
Avg time: 0.0018 s

Test name: get_movie_reviews_sort_pub_date
Test iterations: 10
Full time: 0.040627899987157434 s
Avg time: 0.0041 s

Test name: get_movie_reviews_sort_scores_quality
Test iterations: 10
Full time: 0.02405499995802529 s
Avg time: 0.0024 s

Test name: get_user_liked_movies
Test iterations: 10
Full time: 0.1972946999972919 s
Avg time: 0.01973 s

Test name: get_user_liked_reviews
Test iterations: 10
Full time: 0.9689278900041245 s
Avg time: 0.09689 s

Test name: get_movie_scores_quality
Test iterations: 10
Full time: 0.014084299997193739 s
Avg time: 0.0014 s

Test name: get_movie_good_ratings_count
Test iterations: 10
Full time: 0.020812299975659698 s
Avg time: 0.0021 s

Running write benchmarks for MongoDB...
Test name: add_bookmark
Test iterations: 10
Full time: 0.013008399997488596 s
Avg time: 0.0013 s

Test name: add_review
Test iterations: 10
Full time: 0.36797089996980503 s
Avg time: 0.0368 s

Test name: add_movie_score
Test iterations: 10
Full time: 0.26616460003424436 s
Avg time: 0.0266 s

Test name: add_review_score
Test iterations: 10
Full time: 0.23797979997470975 s
Avg time: 0.0238 s
"""
import argparse
import sys

from pymongo import MongoClient

from misc import upload_users_bookmarks, upload_movies_and_reviews
from config import DB_NAME, MONGO_HOST, MONGO_PORT
import tests


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true",
                        help="create test benchmark data")
    parser.add_argument("-r", "--read", action="store_true",
                        help="start read benchmarks")
    parser.add_argument("-w", "--write", action="store_true",
                        help="start read benchmarks")
    return parser


if __name__ == "__main__":
    ap = create_argument_parser()
    argv = ap.parse_args(sys.argv[1:])

    if argv.create:
        print("Creating data for benchmarks")
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = client.get_database(DB_NAME)
        upload_users_bookmarks(db)
        upload_movies_and_reviews(db)

    if argv.read:
        print("Running read benchmarks for MongoDB...")
        for test in tests.READ_TESTS:
            test()

    if argv.write:
        print("Running write benchmarks for MongoDB...")
        for test in tests.WRITE_TESTS:
            test()
