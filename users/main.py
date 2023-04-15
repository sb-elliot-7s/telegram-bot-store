import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, status, HTTPException

from constants import Topic
from db import user_collection
from kafka_service import KafkaConsumerService
from repository import UserRepository
from services import UserServices

loop = asyncio.get_event_loop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_consumer = KafkaConsumerService(
        user_repository=UserRepository(collection=user_collection),
        topics=[Topic.SAVE_USER.value, Topic.UPDATE_USER.value]
    )
    loop.create_task(kafka_consumer.consume())
    yield
    await kafka_consumer.close()


app = FastAPI(lifespan=lifespan)


@app.get(path='/users/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    if (user := await UserServices(repository=UserRepository(collection=user_collection))
            .get_user(user_id=user_id)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
