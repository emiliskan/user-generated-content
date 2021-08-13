import os

BATCH_SIZE = 1000
FLUSH_PERIOD = 5
IDLE_TIMEOUT = 5

ETL_STORAGE_TABLE = os.environ.get("ETL_STORAGE_TABLE", "movie_progress")
ETL_BACKOFF_MAX_TIME = int(os.environ.get("ETL_BACKOFF_MAX_TIME", 300))

KAFKA_DSN = {
    # TODO, ask from @emiliskan
    "topics":  os.environ.get("KAFKA_TOPIC", "views"),
    "group_id": os.environ.get("KAFKA_CONSUMER_GROUP", "echo-messages-to-stdout"),
    "bootstrap_servers": os.environ.get("KAFKA_SERVERS", ("localhost:9092", "broker:29092")),
    "auto_offset_reset": "earliest",
}

CLICKHOUSE_DSN = {

}