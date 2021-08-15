CLICKHOUSE_HOST = "localhost"
UNIQUE_IDS = 10000
MAX_MOVIE_DURATION = 360
BATCH_SIZE = 1000
BATCH_COUNT = 10_000

BENCHMARK_ITERATIONS = 10
TABLE = "benchmarks_db.events"

REQUESTS = {
    "unique_user_exact": f"select uniqExact(user_id) from {TABLE}",
    "unique_movies_exact": f"select uniqExact(movie_id) from {TABLE}",
    "unique_movies_count": f"select count(distinct movie_id) from {TABLE}",
    "unique_users_count": f"select count(distinct user_id) from {TABLE}",
    "user_stat": f"SELECT user_id, sum(viewed_frame), max(viewed_frame)\
     FROM {TABLE} GROUP by user_id"
}
