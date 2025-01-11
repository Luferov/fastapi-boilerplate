from typing import Annotated

from fastapi import Depends

from src.apps.users.repositories.users import UsersRepositoryFactoryImpl, UsersRepositoryFactoryProtocol

from .enums import UsersProviderEnum
from .services import UsersServiceImpl, UsersServiceProtocol
from .use_cases import UsersUseCaseImpl, UsersUseCaseProtocol

# --- repositories ---


def get_users_factory_repository(provider: UsersProviderEnum) -> UsersRepositoryFactoryProtocol:
    return UsersRepositoryFactoryImpl(provider)


UsersFactoryRepository = Annotated[UsersRepositoryFactoryProtocol, Depends(get_users_factory_repository)]

# -- services ---


def get_users_service(users_factory_repository: UsersFactoryRepository) -> UsersServiceProtocol:
    return UsersServiceImpl(users_factory_repository)


UsersService = Annotated[UsersServiceProtocol, Depends(get_users_service)]

# --- use_cases ---


def get_users_use_case(users_service: UsersService) -> UsersUseCaseProtocol:
    return UsersUseCaseImpl(users_service)


UsersUseCase = Annotated[UsersUseCaseProtocol, Depends(get_users_use_case)]
