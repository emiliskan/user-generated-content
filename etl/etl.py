import datetime
import json
import time

import backoff

from kafka import KafkaConsumer
from clickhouse_driver import Client as ClickHouseClient
from setting import (ETL_BACKOFF_MAX_TIME, ETL_STORAGE_TABLE, BATCH_SIZE,
                     FLUSH_PERIOD, IDLE_TIMEOUT, KAFKA_DSN, CLICKHOUSE_DSN)

# TODO add logger
logger = None


@backoff.on_exception(backoff.expo, ConnectionError, max_time=ETL_BACKOFF_MAX_TIME)
def connect_storage(dns: dict) -> ClickHouseClient:
    return ClickHouseClient(**dns)


@backoff.on_exception(backoff.expo, ConnectionError, max_time=ETL_BACKOFF_MAX_TIME)
def connect_consumer(dns: dict) -> KafkaConsumer:
    return KafkaConsumer(**dns)


def transform(value: str) -> dict:
    value = json.loads(value)
    record = {
        'user_id': str(value.get('user_id')),
        'movie_id': str(value.get('movie_id')),
        'viewed_frame': int(value.get('viewed_frame')),
        'created_at': datetime.datetime.now(),
    }
    return record


def start_etl():
    consumer = connect_consumer(KAFKA_DSN)
    storage = connect_storage(CLICKHOUSE_DSN)

    flush_time_stamp = time.time()
    values = []
    for msg in consumer:
        record = transform(msg.value)
        values.append(record)

        if len(values) > BATCH_SIZE or (time.time() - flush_time_stamp) > FLUSH_PERIOD:
            storage.execute(f"INSERT INTO {ETL_STORAGE_TABLE} VALUES",
                            values, types_check=True)
            values.clear()
            flush_time_stamp = time.time()


if __name__ == "__main__":
    start_etl()


