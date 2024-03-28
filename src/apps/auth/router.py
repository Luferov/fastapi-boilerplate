from fastapi import APIRouter

from .auth import auth_backend, fastapi_users
from .schemas import UserCreate, UserRead

__all__ = ('router',)

router = APIRouter(prefix='/auth', tags=['Auth'])

router.include_router(fastapi_users.get_auth_router(auth_backend))

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
