import os
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent


class TestSettings(BaseSettings):
    es_host = Field("localhost", env="ELASTIC_HOST")
    es_port = Field("9200", env="ELASTIC_PORT")
    redis_host = Field("localhost", env="REDIS_HOST")
    redis_port = Field("6379", env="REDIS_PORT")
    backend_api_host = Field("localhost", env="BACKEND_API_HOST")
    backend_api_port = Field("8000", env="BACKEND_API_PORT")
    base_dir = Field(BASE_DIR, env="BASE_DIR", description="Путь к корневой папке тестов.")
    test_data_dir = Field(
        os.path.join(BASE_DIR, "testdata"),
        description="Путь к папке для создания индекса и данных для тестов.",
    )
