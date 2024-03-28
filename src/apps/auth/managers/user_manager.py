from typing import Annotated

from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.settings import settings

from ..models import USER_ID, User
from ..repositories import BaseUserRepository, get_user_repository


class UserManager(IntegerIDMixin, BaseUserManager[User, USER_ID]):
    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key


async def get_user_manager(user_repository: Annotated[BaseUserRepository, Depends(get_user_repository)]):
    """
    Получаем менеджера для работы с пользователем.
    """
    return UserManager(user_repository)
