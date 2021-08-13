from functools import lru_cache
from fastapi import Depends
from kafka import KafkaProducer

from db.kafka_producer import get_kafka


class MoviesService:

    def __init__(self, kafka):
        self.kafka: KafkaProducer = kafka

    async def save_movie_progress(self, movie_id: str, user_id: str, viewed_frame: str) -> None:
        self.kafka.send(
            topic="movies_progress",
            key=str.encode(movie_id+user_id, 'utf-8'),
            value=str.encode(viewed_frame, 'utf-8'))


@lru_cache(maxsize=128)
def get_movies_service(kafka: KafkaProducer = Depends(get_kafka)) -> MoviesService:
    return MoviesService(kafka)
