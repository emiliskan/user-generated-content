import os
import yaml
import pathlib
import sentry_sdk

BATCH_SIZE = 2
FLUSH_PERIOD = 5
IDLE_TIMEOUT = 5


logconfig = pathlib.Path(__file__).parent.joinpath("logger_config.yaml")
with open(logconfig) as stream:
    LOGGER_CONFIG = yaml.safe_load(stream)

ETL_BACKOFF_MAX_TIME = int(os.environ.get("ETL_BACKOFF_MAX_TIME", 300))

KAFKA_HOST = os.environ.get("KAFKA_HOST", "rc1a-mi7khra801ifkpfs.mdb.yandexcloud.net")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9091")
KAFKA_SERVERS = [f'{KAFKA_HOST}:{KAFKA_PORT}']
KAFKA_TOPICS = os.environ.get("KAFKA_TOPIC", "movies_progress")
KAFKA_SECURITY_PROTOCOL = os.environ.get("KAFKA_SECURITY_PROTOCOL", "SASL_SSL")
KAFKA_SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM", "SCRAM-SHA-512")
KAFKA_SASL_PLAIN_PASSWORD = os.getenv("KAFKA_SASL_PLAIN_PASSWORD", "aaaaaaaa")
KAFKA_SASL_PLAIN_USERNAME = os.getenv("KAFKA_SASL_PLAIN_USERNAME", "ugc_api")
KAFKA_SSL_CAFILE = os.getenv("KAFKA_SSL_CAFILE", "$HOME/.kafka/YandexCA.crt")
SENTRY_DSN = os.getenv("SENTRY_DSN", "https://985de561392e4d6391fb209958b7eda5@o977346.ingest.sentry.io/5933885")

KAFKA_DSN = {
    "group_id": os.environ.get("KAFKA_CONSUMER_GROUP", "echo-messages-to-stdout"),
    "bootstrap_servers": KAFKA_SERVERS,
    "security_protocol": KAFKA_SECURITY_PROTOCOL,
    "sasl_mechanism": KAFKA_SASL_MECHANISM,
    "sasl_plain_password": KAFKA_SASL_PLAIN_PASSWORD,
    "sasl_plain_username": KAFKA_SASL_PLAIN_USERNAME,
    "ssl_cafile": KAFKA_SSL_CAFILE,
    "auto_offset_reset": "earliest",
}

# ClickHouse
CLICKHOUSE_STORAGE_TABLE = os.environ.get("CLICKHOUSE_STORAGE_TABLE", "movies_progress")
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB", "db_ucg")
CLICKHOUSE_SSL_CAFILE = os.getenv("CLICKHOUSE_SSL_CAFILE", "$HOME/.clickhouse/CA.crt")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "etl_user")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "password")

CLICKHOUSE_DSN = {
    "host": os.environ.get("CLICKHOUSE_HOST", "rc1a-obil11vzkl8sxsc4.mdb.yandexcloud.net"),
    "database": CLICKHOUSE_DB,
    "secure": True,
    "user": CLICKHOUSE_USER,
    "password": CLICKHOUSE_PASSWORD,
    "ca_certs": CLICKHOUSE_SSL_CAFILE
}


sentry_sdk.init(
    SENTRY_DSN
)
