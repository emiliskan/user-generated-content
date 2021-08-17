"""
Total insert operation time: 280.202

Tests results without load:
unique_user_exact
    total time: 0.363
    average time: 0.036
unique_movies_exact:
    total time: 0.346
    average time: 0.035
unique_movies_count:
    total time: 0.340
    average time: 0.034
unique_users_count:
    total time: 0.334
    average time: 0.033
user_stat:
    total time: 0.897
    average time: 0.090

Tests results under load:
unique_user_exact:
    total time: 0.462
    average time: 0.046
unique_movies_exact:
    total time: 0.456
    average time: 0.046
unique_movies_count
    total time: 0.444
    average time: 0.044
unique_users_count:
    total time: 0.438
    average time: 0.044
user_stat
    total time: 1.322
    average time: 0.132
"""
import argparse
import datetime
import random
import time
import sys
from typing import Iterator, List

from clickhouse_driver import Client

from research.config import (CLICKHOUSE_HOST, BATCH_SIZE, BATCH_COUNT,
                             BENCHMARK_ITERATIONS, CLICKHOUSE_REQUESTS,
                             FAKE_USER_IDS, FAKE_MOVIE_IDS, MAX_MOVIE_DURATION)

client = Client(CLICKHOUSE_HOST)


def generate_row() -> dict:
    return {
        'user_id': random.choice(FAKE_USER_IDS),
        'movie_id': random.choice(FAKE_MOVIE_IDS),
        'viewed_frame': random.randint(1, MAX_MOVIE_DURATION),
        'event_time': datetime.datetime.now(),
    }


def generate_batch(size: int) -> List[dict]:
    return [generate_row() for _ in range(size)]


def generate_fake_data(size: int, count: int) -> Iterator:
    return (generate_batch(size) for _ in range(count))


def execute_timer(query: str, iteration=1, verbose=False):
    operation_time = []
    for i in range(1, iteration+1):
        start_time = time.perf_counter()
        client.execute(query)
        ot = time.perf_counter() - start_time
        if verbose:
            print(f"attempt {i}/{iteration}: {ot}")
        operation_time.append(ot)

    total_time = sum(operation_time)
    avg_time = total_time / iteration
    print(f"\ntotal time: {total_time:.3f}")
    print(f"average time: {avg_time:.3f}")


def fill_in_database(size: int, count: int):
    operation_time = []
    for values in generate_fake_data(size, count):
        start_time = time.perf_counter()
        client.execute("INSERT INTO benchmarks_db.events VALUES", values)
        ot = time.perf_counter() - start_time
        operation_time.append(ot)
        print(f"insert batch: {ot:.3f}")

    total_time = sum(operation_time)
    print(f"Total insert operation time: {total_time:.3f}")


def run_benchmarks(requests: dict, iteration: int, verbose=False):
    print("Running benchmarks for Clickhouse:")
    for name, query in requests.items():
        print(f"start: {name}")
        execute_timer(query, iteration, verbose)
        print("----------\n")


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
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

    if argv.fill:
        fill_in_database(BATCH_SIZE, BATCH_COUNT)

    if argv.bench:
        run_benchmarks(CLICKHOUSE_REQUESTS, argv.iter, argv.verbose)
