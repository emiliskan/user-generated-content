"""
Total insert operation time: 403.185

Tests results without load:
unique_user_exact:
    total time: 3.618
    average time: 0.362
unique_movies_exact:
    total time: 3.103
    average time: 0.310
unique_movies_count:
    total time: 2.092
    average time: 0.209
unique_users_count:
    total time: 2.089
    average time: 0.209
user_stat:
    total time: 4.862
    average time: 0.486

Tests results under load:
unique_user_exact:
    total time: 3.515
    average time: 0.351
unique_movies_exact:
    total time: 3.519
    average time: 0.352
unique_movies_count:
    total time: 2.179
    average time: 0.218
unique_users_count:
    total time: 2.186
    average time: 0.219
user_stat:
    total time: 5.559
    average time: 0.556

"""
import argparse
import datetime
import random
import sys
import time
from typing import Iterator, List

import vertica_python

from research.config import (VERTICA_DNS, BATCH_SIZE, BATCH_COUNT,
                             FAKE_USER_IDS, FAKE_MOVIE_IDS, MAX_MOVIE_DURATION,
                             BENCHMARK_ITERATIONS, VERTICA_REQUESTS)


def generate_row() -> tuple:
    return (
        random.choice(FAKE_USER_IDS),
        random.choice(FAKE_MOVIE_IDS),
        random.randint(1, MAX_MOVIE_DURATION),
        datetime.datetime.now()
    )


def generate_batch(size: int) -> List[tuple]:
    return [generate_row() for _ in range(size)]


def generate_fake_data(size: int, count: int) -> Iterator:
    return (generate_batch(size) for _ in range(count))


def execute_timer(query: str, iteration=1, verbose=False):
    operation_time = []
    with vertica_python.connect(**VERTICA_DNS) as connection:
        cursor = connection.cursor()
        for i in range(1, iteration+1):
            start_time = time.perf_counter()
            cursor.execute(query)
            ot = time.perf_counter() - start_time
            if verbose:
                print(f"attempt {i}/{iteration}: {ot}")
            operation_time.append(ot)

    total_time = sum(operation_time)
    avg_time = total_time / iteration
    print(f"\ntotal time: {total_time:.3f}")
    print(f"average time: {avg_time:.3f}")


def create_table():
    with vertica_python.connect(**VERTICA_DNS) as connection:
        cursor = connection.cursor()
        cursor.execute("""DROP TABLE IF EXISTS events""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id           UUID DEFAULT UUID_GENERATE(),
            user_id      UUID    NOT NULL,
            movie_id     UUID    NOT NULL,
            viewed_frame INTEGER NOT NULL,
            event_time   DATETIME NOT NULL)
        """)


def fill_in_database(size: int, count: int):
    operation_time = []
    with vertica_python.connect(**VERTICA_DNS) as connection:
        cursor = connection.cursor()
        for values in generate_fake_data(size, count):
            start_time = time.perf_counter()
            cursor.executemany(
                "INSERT INTO events (user_id, movie_id, viewed_frame, event_time) VALUES (%s,%s,%s,%s)",
                values
            )
            ot = time.perf_counter() - start_time
            operation_time.append(ot)
            print(f"insert batch: {ot:.3f}")

    total_time = sum(operation_time)
    print(f"Total insert operation time: {total_time:.3f}")


def run_benchmarks(requests: dict, iteration: int, verbose=False):
    print("Running benchmarks for Vertica:")
    for name, query in requests.items():
        print(f"start: {name}")
        execute_timer(query, iteration, verbose)
        print("----------\n")


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true",
                        help="create test table")
    parser.add_argument("-f", "--fill", action="store_true",
                        help="filling in database fake data")
    parser.add_argument("-b", "--bench", action="store_true",
                        help="run database benchmarks")
    parser.add_argument("-i", "--iter", type=int,
                        default=BENCHMARK_ITERATIONS,
                        help="benchmark iteration")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show intermediate results")
    return parser


if __name__ == "__main__":
    ap = create_argument_parser()
    argv = ap.parse_args(sys.argv[1:])

    if argv.create:
        create_table()

    if argv.fill:
        fill_in_database(BATCH_SIZE, BATCH_COUNT)

    if argv.bench:
        run_benchmarks(VERTICA_REQUESTS, argv.iter, argv.verbose)
