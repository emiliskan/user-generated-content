import abc
from typing import List
import backoff
from clickhouse_driver import Client
import clickhouse_driver.errors

from setting import ETL_BACKOFF_MAX_TIME, CLICKHOUSE_DSN, CLICKHOUSE_STORAGE_TABLE


class Storage(abc.ABC):
    def __call__(self):
        return self

    @abc.abstractmethod
    def load(self, values: List[dict]):
        pass


class ClickHouseClient(Storage):
    def __init__(self, **dns):
        self.client = Client(**dns)
        self.storage_table = CLICKHOUSE_STORAGE_TABLE

    @backoff.on_exception(backoff.expo,
                          clickhouse_driver.errors.SocketTimeoutError,
                          max_time=ETL_BACKOFF_MAX_TIME)
    def load(self, values: List[dict]):
        self.client.execute(f'INSERT INTO {self.storage_table} VALUES',
                            values, types_check=True)


def get_current_storage() -> Storage:
    return ClickHouseClient(**CLICKHOUSE_DSN)
