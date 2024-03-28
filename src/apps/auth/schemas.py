from fastapi_users import schemas

from src.apps.auth.models import USER_ID


class UserRead(schemas.BaseUser[USER_ID]):
    ...


class UserCreate(schemas.BaseUserCreate):
    ...


class UserUpdate(schemas.BaseUserUpdate):
    ...
