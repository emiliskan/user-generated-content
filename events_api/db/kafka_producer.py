from kafka import KafkaProducer
from core import config

kafka_producer_client = KafkaProducer(bootstrap_servers=config.KAFKA_SERVERS)


async def get_kafka() -> KafkaProducer:
    return kafka_producer_client
