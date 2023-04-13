from abc import ABC, abstractmethod

from schemas import UpdateUserSchema


class UserRepositoryProtocol(ABC):
    @abstractmethod
    async def save_user(self, user_data: dict):
        pass

    @abstractmethod
    async def get_user(self, user_id: int):
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user_data: UpdateUserSchema): pass
