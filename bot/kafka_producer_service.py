from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from schemas import KafkaSettingsSchema


@dataclass
class KafkaService:

    @staticmethod
    async def produce(value: dict, topic: str):
        producer = AIOKafkaProducer(**KafkaSettingsSchema().dict())
        await producer.start()
        try:
            await producer.send_and_wait(topic=topic, value=value)
        finally:
            await producer.stop()
