from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorCollection

from protocols.service_center_repository_protocol import ServiceCenterRepositoryProtocol
from schemas import ServiceCenterSchema


@dataclass
class ServiceCenterRepository(ServiceCenterRepositoryProtocol):
    collection: AsyncIOMotorCollection

    async def get_service_center(self, city: str):
        cursor = self.collection.find({'address': {'$regex': city, '$options': 'si'}})
        return [ServiceCenterSchema(**i).dict(by_alias=False) async for i in cursor]

    async def get_all_service_center(self) -> list[ServiceCenterSchema]:
        return [ServiceCenterSchema(**i) async for i in self.collection.find()]
