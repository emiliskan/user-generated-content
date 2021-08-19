import datetime
import json
import time
import uuid
import logging

import logging.config

import backoff
from kafka import KafkaConsumer

from setting import (ETL_BACKOFF_MAX_TIME, BATCH_SIZE, LOGGER_CONFIG,
                     FLUSH_PERIOD, IDLE_TIMEOUT, KAFKA_DSN, KAFKA_TOPICS)

from storage import get_current_storage

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger("ugc_etl")


@backoff.on_exception(backoff.expo, ConnectionError,
                      max_time=ETL_BACKOFF_MAX_TIME)
def connect_consumer(topics: str, dns: dict) -> KafkaConsumer:
    return KafkaConsumer(topics, **dns)


def transform(value: str) -> dict:
    value = json.loads(value)
    record = {
        'id': str(uuid.uuid4()),
        'user_id': str(value.get('user_id')),
        'movie_id': str(value.get('movie_id')),
        'viewed_frame': int(value.get('viewed_frame')),
        'event_time': datetime.datetime.now(),
    }
    return record


def start_etl():
    consumer = connect_consumer(KAFKA_TOPICS, KAFKA_DSN)
    logger.info("connect to consumer")

    storage = get_current_storage()
    logger.info("connect to storage")

    while True:
        flush_time_stamp = time.time()
        values = []
        for msg in consumer:
            record = transform(msg.value)
            values.append(record)

            if (len(values) > BATCH_SIZE or
                    (time.time() - flush_time_stamp) > FLUSH_PERIOD):
                try:
                    storage.load(values)
                except Exception as e:
                    logger.error(e)
                else:
                    values.clear()
                    logger.info("data is uploaded to storage")

                flush_time_stamp = time.time()

        if len(values):
            logger.info(f"no data, idle {IDLE_TIMEOUT} s")
            time.sleep(IDLE_TIMEOUT)


if __name__ == "__main__":
    logger.info("start ugc etl")
    start_etl()
