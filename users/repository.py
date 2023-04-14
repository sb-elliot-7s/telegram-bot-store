from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorCollection

from protocols.repositories_protocol import UserRepositoryProtocol
from schemas import UpdateUserSchema


@dataclass
class UserRepository(UserRepositoryProtocol):
    collection: AsyncIOMotorCollection

    async def save_user(self, user_data: dict):
        result = await self.collection.insert_one(document=user_data)
        return True if result.insert_id else False

    async def get_user(self, user_id: int | str):
        return await self.collection.find_one(filter={'_id': str(user_id)})

    async def update_user(self, user_id: int, user_data: UpdateUserSchema):
        await self.collection.update_one(
            filter={'_id': user_id},
            update={'$set': user_data.dict(exclude_none=True, exclude={'id'})})
