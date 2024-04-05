from src.core.pagination import ModelPaginator

from .schemas import UserRead


class UserPagination(ModelPaginator[UserRead]):
    ...