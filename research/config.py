import uuid

UNIQUE_IDS = 10000
MAX_MOVIE_DURATION = 360
BATCH_SIZE = 1000
BATCH_COUNT = 10_000
BENCHMARK_ITERATIONS = 10

FAKE_USER_IDS = [uuid.uuid4() for _ in range(UNIQUE_IDS)]
FAKE_MOVIE_IDS = [uuid.uuid4() for _ in range(UNIQUE_IDS)]

CLICKHOUSE_HOST = "localhost"
TABLE = "benchmarks_db.events"
CLICKHOUSE_REQUESTS = {
    "unique_user_exact": f"select uniqExact(user_id) from {TABLE}",
    "unique_movies_exact": f"select uniqExact(movie_id) from {TABLE}",
    "unique_movies_count": f"select count(distinct movie_id) from {TABLE}",
    "unique_users_count": f"select count(distinct user_id) from {TABLE}",
    "user_stat": f"SELECT user_id, sum(viewed_frame), max(viewed_frame)\
     FROM {TABLE} GROUP by user_id"
}

VERTICA_DNS = {
    "host": "127.0.0.1",
    "port": 5433,
    "user": "dbadmin",
    "password": '',
    "database": "docker",
    "autocommit": True,
}
VERTICA_REQUESTS = {
    "unique_user_exact": f"select distinct user_id from events",
    "unique_movies_exact": f"select distinct movie_id from events",
    "unique_movies_count": f"select count(distinct movie_id) from events",
    "unique_users_count": f"select count(distinct user_id) from events",
    "user_stat": f"SELECT user_id, sum(viewed_frame), max(viewed_frame)\
     FROM events GROUP by user_id"
}