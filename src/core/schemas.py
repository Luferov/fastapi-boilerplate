from typing import Generic, TypeVar

from pydantic import BaseModel, PositiveInt

PaginationItem = TypeVar('PaginationItem', bound=BaseModel)

class CreateBaseModel(BaseModel):
    """
    Контракт для создания моделей.
    """

    id: int | None = None


class UpdateBaseModel(BaseModel):
    """
    Контракт обновления моделей.
    """

    id: int


class StatusOkSchema(BaseModel):
    status: str = 'ok'


class PaginationSchema(BaseModel):
    page: PositiveInt
    page_size: PositiveInt


class PaginationResultSchema(PaginationSchema, Generic[PaginationItem]):

    total_pages: PositiveInt
    count: PositiveInt
    items: list[PaginationItem]
