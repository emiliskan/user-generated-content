import os

BATCH_SIZE = 1000
FLUSH_PERIOD = 5
IDLE_TIMEOUT = 5

ETL_STORAGE_TABLE = os.environ.get("ETL_STORAGE_TABLE", "movie_progress")
ETL_BACKOFF_MAX_TIME = int(os.environ.get("ETL_BACKOFF_MAX_TIME", 300))

KAFKA_HOST = os.environ.get("KAFKA_HOST", "rc1a-mi7khra801ifkpfs.mdb.yandexcloud.net")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9091")
KAFKA_TOPICS = os.environ.get("KAFKA_TOPIC", "movies_progress"),
KAFKA_DSN = {
    "group_id": os.environ.get("KAFKA_CONSUMER_GROUP", "echo-messages-to-stdout"),
    "bootstrap_servers": (f"{KAFKA_HOST}:{KAFKA_PORT}", ),
    "security_protocol": os.environ.get("KAFKA_SECURITY_PROTOCOL", "SASL_SSL"),
    "auto_offset_reset": "earliest",
}

CLICKHOUSE_DSN = {
    "host": os.environ.get("CLICKHOUSE_HOST", "localhost"),
}
