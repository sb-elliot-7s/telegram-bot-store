from aiokafka import AIOKafkaConsumer

from constants import Topic
from protocols.repository_protocol import PaymentsRepositoryProtocol
from schemas import KafkaSettingsSchema, PaymentResponseSchema


class KafkaConsumerService:
    def __init__(self, topics: list[str], payments_repository: PaymentsRepositoryProtocol):
        self.payments_repository = payments_repository
        self.topics = topics

    async def save_payments_handler(self, message):
        payment_schema = PaymentResponseSchema(**message.value)
        await self.payments_repository.save_payments_data(payment_data=payment_schema)

    async def consume(self):
        consumer = AIOKafkaConsumer(*self.topics, **KafkaSettingsSchema().dict())
        await consumer.start()
        try:
            async for message in consumer:
                match message.topic:
                    case Topic.SAVE_PAYMENTS_DATA.value:
                        await self.save_payments_handler(message=message)
        finally:
            await consumer.stop()
