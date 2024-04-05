import contextlib
from typing import Generic, Protocol, Self, Type, TypeVar, cast, get_args

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import Base
from src.core.pagination import ModelPaginator
from src.core.utils.exceptions import ModelNotFoundException

from ..schemas import CreateBaseModel, PaginationItem, PaginationSchema, UpdateBaseModel

ModelType = TypeVar('ModelType', bound=Base, covariant=True)
ReadSchemaType = TypeVar('ReadSchemaType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=CreateBaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=UpdateBaseModel)


class BaseRepositoryProtocol(Protocol[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]):
    async def get(self: Self, id: int) -> ReadSchemaType:
        ...

    async def get_or_none(self: Self, id: int) -> ReadSchemaType | None:
        ...

    async def get_by_ids(self: Self, ids: list[int | str]) -> list[ReadSchemaType]:
        ...

    async def create(self: Self, create_object: CreateSchemaType) -> ReadSchemaType:
        ...

    async def bulk_create(self, create_objects: list[CreateSchemaType]) -> list[ReadSchemaType]:
        ...

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType:
        ...

    async def bulk_update(self, update_objects: list[UpdateSchemaType]) -> None:
        ...

    async def upsert(self, create_object: CreateSchemaType) -> ReadSchemaType:
        ...

    async def delete(self, id: int) -> bool:
        ...


class BaseRepositoryImpl(Generic[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]):
    __orig_bases__: 'tuple[Type[BaseRepositoryImpl[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]]]'

    model_type: Type[ModelType]
    read_schema_type: Type[ReadSchemaType]

    def __init__(self: Self, session: AsyncSession):
        """
        Base CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.session = session

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, '__orig_bases__'):
            raise ValueError('Repository must be implements by BaseImplRepository')
        base_repository_generic, *_ = cls.__orig_bases__  # type: ignore
        cls.model_type, cls.read_schema_type, *_ = cast(
            tuple[Type[ModelType], Type[ReadSchemaType], Type[CreateSchemaType], Type[UpdateSchemaType]],
            get_args(base_repository_generic),
        )
        return super().__init_subclass__()

    async def get(self: Self, id: int) -> ReadSchemaType:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.id == id)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, id)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def get_or_none(self: Self, id: int) -> ReadSchemaType | None:
        with contextlib.suppress(ModelNotFoundException):
            return await self.get(id)
        return None

    async def get_by_ids(self: Self, ids: list[int | str]) -> list[ReadSchemaType]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.id.in_(ids))
            models = (await s.execute(statement)).scalars().all()
            return [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]

    async def create(self: Self, create_object: CreateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            statement = (
                sa.insert(self.model_type).values(**create_object.model_dump(exclude={'id'})).returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one()
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def bulk_create(self, create_objects: list[CreateSchemaType]) -> list[ReadSchemaType]:
        async with self.session as s, s.begin():
            statement = sa.insert(self.model_type).returning(self.model_type)
            models = (await s.scalars(statement, [x.model_dump() for x in create_objects])).all()
            return [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            pk = update_object.id
            statement = (
                sa.update(self.model_type)
                .where(self.model_type.id == pk)
                .values(update_object.model_dump(exclude={'id'}, exclude_unset=True))
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one()
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def bulk_update(self, update_objects: list[UpdateSchemaType]) -> None:
        async with self.session as s, s.begin():
            statement = sa.update(self.model_type)
            await s.execute(statement, [x.model_dump(exclude_unset=True) for x in update_objects])

    async def upsert(self: Self, create_object: CreateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            primary_keys = [key.name for key in sa.inspect(self.model_type).primary_key]
            statement = (
                insert(self.model_type)
                .values(**create_object.model_dump())
                .on_conflict_do_update(
                    index_elements=primary_keys, set_=create_object.model_dump(exclude={*primary_keys})
                )
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one()
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def delete(self, id: int) -> bool:
        async with self.session as s, s.begin():
            statement = sa.delete(self.model_type).where(self.model_type.id == id)
            await s.execute(statement)
            return True

    async def get_list(
        self,
        model_paginator_type: Type[ModelPaginator[ReadSchemaType]],
        pagination: PaginationSchema
    ) -> PaginationSchema[ReadSchemaType]:
        statement = sa.select(self.model_type)
        model_paginator = model_paginator_type(self.session)
        return await model_paginator.get_list(
            statement=statement,
            pagination=pagination
        )

