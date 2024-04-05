import math
from typing import ClassVar, Generic, Protocol, Self, Type, cast, get_args

import sqlalchemy as sa
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.base_repository import ModelType

from .schemas import PaginationItem, PaginationResultSchema, PaginationSchema


class PaginatorProtocol(Protocol):

    pagination: PaginationSchema

    @property
    def page(self) -> int:
        ...

    @property
    def page_size(self) -> int:
        ...

    def total_pages(self: Self, count: int) -> int:
        ...

    def offset(self: Self) -> int:
        ...


class OffsetPaginator:

    def __init__(self, pagination: PaginationSchema) -> None:
        self.pagination = pagination

    @property
    def page(self) -> int:
        return self.pagination.page

    @property
    def page_size(self) -> int:
        return self.pagination.page_size

    def total_pages(self: Self, count: int) -> int:
        return math.ceil(count / self.pagination.page_size)

    def offset(self: Self) -> int:
        return max((self.pagination.page - 1) * self.pagination.page_size, 0)


async def get_paginator(pagination: PaginationSchema) -> PaginatorProtocol:
    return OffsetPaginator(pagination)


class ModelPaginator(Generic[PaginationItem]):
    __orig_bases__: 'tuple[Type[ModelPaginator[PaginationItem]]]'

    paginator_type: ClassVar[Type[OffsetPaginator]]  = OffsetPaginator

    pagination_item_type: Type[PaginationItem]

    def __init__(self: Self, session: AsyncSession) -> None:
        self.session = session

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, '__orig_bases__'):
            raise ValueError('Model pagination must be implements by ModelPaginator')
        base_repository_generic, *_ = cls.__orig_bases__  # type: ignore
        cls.pagination_item_type, *_ = cast(
            tuple[Type[PaginationItem]],
            get_args(base_repository_generic),
        )

    async def get_list(self, statement: Select[tuple[ModelType]], pagination: PaginationSchema) -> PaginationResultSchema[PaginationItem]:
        paginator = self.paginator_type(pagination)
        async with self.session as s:
            count = (await s.execute(sa.select(sa.func.count()).select_from(statement.subquery()))).scalar_one()
            statement_items = statement.limit(paginator.page_size).offset(paginator.offset())
            models = (await s.execute(statement_items)).scalars().all()

            return PaginationResultSchema(
                total_pages=paginator.total_pages(count),
                count=count,
                page=paginator.page,
                page_size=paginator.page_size,
                items=[self.pagination_item_type.model_validate(model) for model in models],
            )