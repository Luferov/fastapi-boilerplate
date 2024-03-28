from typing import Annotated

from fastapi import Depends
from fastapi_users.db import BaseUserDatabase, SQLAlchemyUserDatabase

from src.apps.auth.models import USER_ID, User
from src.core.db import AsyncSession, get_async_session

__all__ = ('BaseUserRepository', 'get_user_repository')


class BaseUserRepository(BaseUserDatabase[User, USER_ID]):
    ...


class UserRepository(SQLAlchemyUserDatabase[User, USER_ID]):
    ...


async def get_user_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> BaseUserRepository:
    return UserRepository(session, User)
