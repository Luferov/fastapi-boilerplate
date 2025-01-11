from typing import Protocol, Type

from ..enums import UsersProviderEnum
from ..schemas.users import UserSchema


class UsersRepositoryProtocol(Protocol):
    async def get_users(self) -> list[UserSchema]:
        ...


class UsersRepositoryFactoryProtocol(Protocol):
    async def make(self) -> UsersRepositoryProtocol:
        ...


class UsersRepositoryImpl:
    async def get_users(self) -> list[UserSchema]:
        return [
            UserSchema(
                email='luferovvs@yandex.ru',
                username='luferovvs',
                last_name='Луферов',
                first_name='Виктор',
            )
        ]


class UsersRepositoryRedisImpl:
    async def get_users(self) -> list[UserSchema]:
        return [
            UserSchema(
                email='luferovis@yandex.ru',
                username='luferovis',
                last_name='Луферов',
                first_name='Иван',
            )
        ]


class UsersRepositoryFactoryImpl:
    def __init__(self, provider: UsersProviderEnum) -> None:
        self.provider = provider

    async def make(self) -> UsersRepositoryProtocol:
        providers_mapper: dict[UsersProviderEnum, Type[UsersRepositoryImpl | UsersRepositoryRedisImpl]] = {
            UsersProviderEnum.postgres: UsersRepositoryImpl,
            UsersProviderEnum.redis: UsersRepositoryRedisImpl,
        }
        return providers_mapper.get(self.provider, UsersRepositoryImpl)()
