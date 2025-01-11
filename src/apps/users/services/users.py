from typing import Protocol

from src.apps.users.repositories.users import UsersRepositoryFactoryProtocol
from src.apps.users.schemas.users import UserSchema


class UsersServiceProtocol(Protocol):
    async def get_users(self) -> list[UserSchema]:
        ...


class UsersServiceImpl:
    def __init__(self, users_factory_repository: UsersRepositoryFactoryProtocol) -> None:
        self.users_factory_repository = users_factory_repository

    async def get_users(self) -> list[UserSchema]:
        """Получения пользователей


        Тут бывает логика по созданию репозитория или сервиса.

        Returns:
            list[UserSchema]: _description_
        """
        users_service = await self.users_factory_repository.make()
        return await users_service.get_users()
