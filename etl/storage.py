import abc

import backoff
import clickhouse_driver
import clickhouse_driver.errors

from setting import ETL_BACKOFF_MAX_TIME


class Storage(abc.ABC):
    def __call__(self):
        return self

    @abc.abstractmethod
    def load(self, table, values: list):
        pass


class ClickHouseClient(Storage):
    def __init__(self, **dns):
        self.client = clickhouse_driver.Client(dns["host"])

    @backoff.on_exception(backoff.expo,
                          clickhouse_driver.errors.SocketTimeoutError,
                          max_time=ETL_BACKOFF_MAX_TIME)
    def load(self, table: str, values: list):
        self.client.execute(f"INSERT INTO {table} VALUES",
                            values, types_check=True)


def get_current_storage(dns: dict) -> Storage:
    return ClickHouseClient(**dns)
