from abc import ABC, abstractmethod

from schemas import ServiceCenterSchema


class ServiceCenterRepositoryProtocol(ABC):
    @abstractmethod
    async def get_service_center(self, city: str): pass

    @abstractmethod
    async def get_all_service_center(self) -> list[ServiceCenterSchema]: pass
