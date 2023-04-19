import asyncio

from constants import Topic
from db import payments_collection
from kafka_service import KafkaConsumerService
from repository import PaymentsRepository

if __name__ == '__main__':
    kafka_consumer_service = KafkaConsumerService(
        topics=[Topic.SAVE_PAYMENTS_DATA.value],
        payments_repository=PaymentsRepository(payment_collection=payments_collection)
    )
    asyncio.run(kafka_consumer_service.consume())
