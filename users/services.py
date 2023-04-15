from dataclasses import dataclass

from protocols.repositories_protocol import UserRepositoryProtocol


@dataclass
class UserServices:
    repository: UserRepositoryProtocol

    async def get_user(self, user_id: int | str):
        return await self.repository.get_user(user_id=user_id)
