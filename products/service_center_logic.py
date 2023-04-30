from dataclasses import dataclass

from geo_service import GeoService
from protocols.service_center_repository_protocol import ServiceCenterRepositoryProtocol


@dataclass
class ServiceCenterLogic:
    repository: ServiceCenterRepositoryProtocol

    async def get_service_center(self, city: str):
        results = await self.repository.get_service_center(city=city)
        if not results:
            all_service_center = await self.repository.get_all_service_center()
            return await GeoService().calculate_near_city(service_center_cities=all_service_center, query=city)
        return results
