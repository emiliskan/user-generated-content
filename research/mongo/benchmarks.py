#!/usr/bin/env python3

import argparse
import sys

from pymongo import MongoClient

from misc import upload_users_bookmarks, upload_movies_and_reviews
from config import DB_NAME, MONGO_HOST, MONGO_PORT


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
        # upload_users_bookmarks(db)
        upload_movies_and_reviews(db)

    if argv.read:
        print("Running read benchmarks for MongoDB...")
        pass

    if argv.write:
        print("Running write benchmarks for MongoDB...")
        pass
