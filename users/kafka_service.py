from aiokafka import AIOKafkaConsumer

from constants import Topic
from protocols.repositories_protocol import UserRepositoryProtocol
from schemas import KafkaSettingsSchema, UserSchema, UpdateUserSchema


class KafkaConsumerService:
    def __init__(self, topics: list[str], user_repository: UserRepositoryProtocol):
        self.topics = topics
        self.user_repository = user_repository
        self.consumer = AIOKafkaConsumer(*self.topics, **KafkaSettingsSchema().dict())

    async def save_user_handler(self, message):
        schema = UserSchema(**message.value)
        if not await self.user_repository.get_user(user_id=schema.id):
            await self.user_repository.save_user(user_data=schema.to_mongo_object())

    async def update_user_handler(self, message):
        update_schema = UpdateUserSchema(**message.value)
        await self.user_repository.update_user(user_id=update_schema.id, user_data=update_schema)

    async def handle_message(self, message):
        match message.topic:
            case Topic.UPDATE_USER.value:
                await self.update_user_handler(message=message)
            case Topic.SAVE_USER.value:
                await self.save_user_handler(message=message)

    async def consume(self):
        await self.consumer.start()
        try:
            async for message in self.consumer:
                await self.handle_message(message=message)
        finally:
            await self.consumer.stop()

    async def close(self):
        await self.consumer.stop()
