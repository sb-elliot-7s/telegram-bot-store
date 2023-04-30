import numpy as np
from geopy import Location, distance
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

from configs import get_configs
from schemas import ServiceCenterSchema


class GeoService:
    def __init__(self):
        self._nominatim = Nominatim(user_agent=get_configs().app_name, adapter_factory=AioHTTPAdapter)

    async def calculate_near_city(self, service_center_cities: list[ServiceCenterSchema], query: str):
        latitude, longitude = await self.__get_address(query=query)
        results = [
            {
                **s.dict(),
                'distance': distance.distance((s.latitude, s.longitude), (latitude, longitude)).km
            }
            for s in service_center_cities
        ]
        minimum_dist = await self.__get_minimum_distance([i.get('distance') for i in results], 1)
        return [ServiceCenterSchema.from_id_to_object_id(data=i) for i in results if i.get('distance') in minimum_dist]

    async def __get_address(self, query: str):
        async with self._nominatim as geo:
            location: Location = await geo.geocode(query=query)
            return location.latitude, location.longitude

    @staticmethod
    async def __get_minimum_distance(lst, count): return np.partition(lst, count - 1)[:count]
