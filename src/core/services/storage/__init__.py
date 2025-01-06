"""
Предоставляемое приложением файловое хранилище.

Представлено 2 реализации:
- LocalStorage
- S3Storage
"""

from pathlib import Path
from typing import Annotated, AsyncContextManager, Protocol, Self, overload

from fastapi import Depends

from src.core.enums import StorageEnum
from src.settings import SettingsService

from .local_storage import LocalStorage
from .reader import StreamReader as StreamReader
from .reader import StreamReaderProtocol
from .s3_storage import S3Storage
from .schemas import LocalStorageParamsSchema, S3StorageParamsSchema

__all__ = (
    'StorageFactory',
    'StorageService',
    'StorageProtocol',
    'S3Repository',
    'S3RepositoryProtocol',
    'get_storage_factory',
    'StreamReaderProtocol',
    'StreamReader',
)


class StorageProtocol(Protocol):
    async def exists(self, name: str | Path) -> bool:
        """
        Проверка существования файла.
        """
        ...

    async def listdir(self, name: str | Path) -> list[str]:
        """
        Список файлов и директорий в заданной директории.
        """
        ...

    async def is_file(self, name: str | Path) -> bool:
        """
        Возвращает True, если путь существует и это файл.
        """
        ...

    async def is_dir(self, name: str) -> bool:
        """
        Возвращает True, если путь существует и это директория.
        """
        ...

    async def read(self, name: str | Path) -> str | bytes:
        """
        Читает содержимое файла.
        """
        ...

    def stream_read(self, name: str | Path) -> AsyncContextManager[StreamReaderProtocol]:
        """
        Потоковое чтение данных.
        """
        ...

    async def stream_write(self, name: str, stream: StreamReaderProtocol, length: int = -1, part_size: int = 0) -> str:
        """
        Потоковая запись.
        """
        ...

    async def write(self, name: str | Path, content: str | bytes):
        """
        Создает файл или переписывает существующий.

        Возвращает количество записанный байтов.
        """
        ...

    async def delete(self, name: str | Path) -> None:
        """
        Удаляет файл.
        """
        ...


# Протокол интеграции с s3, может быть расширен
class S3RepositoryProtocol(StorageProtocol, Protocol):
    """
    Протокол интеграции с S3 сервисами.
    """

    @property
    def bucket(self) -> str:
        """
        Хранилище в S3.
        """
        ...


async def get_s3_repository(params: S3StorageParamsSchema) -> S3RepositoryProtocol:
    return S3Storage(params)


S3Repository = Annotated[S3RepositoryProtocol, Depends(get_s3_repository)]
StorageParamsSchema = S3StorageParamsSchema | LocalStorageParamsSchema


class StorageFactoryProtocol(Protocol):
    @overload
    async def make(self: Self, kind: StorageEnum, params: S3StorageParamsSchema) -> StorageProtocol:
        ...

    @overload
    async def make(self: Self, kind: StorageEnum, params: LocalStorageParamsSchema) -> StorageProtocol:
        ...

    async def make(self, kind: StorageEnum, params: StorageParamsSchema) -> StorageProtocol:
        ...


class StorageFactoryImpl:
    @overload
    async def make(self: Self, kind: StorageEnum, params: S3StorageParamsSchema) -> StorageProtocol:
        ...

    @overload
    async def make(self: Self, kind: StorageEnum, params: LocalStorageParamsSchema) -> StorageProtocol:
        ...

    async def make(self: Self, kind: StorageEnum, params: StorageParamsSchema) -> StorageProtocol:
        if kind == StorageEnum.S3 and isinstance(params, S3StorageParamsSchema):
            return await self.make_s3_storage(params)
        elif kind == StorageEnum.LOCAL and isinstance(params, LocalStorageParamsSchema):
            return await self.make_local_storage(params)
        raise NotImplementedError

    async def make_s3_storage(self: Self, params: S3StorageParamsSchema) -> StorageProtocol:
        return S3Storage(params)

    async def make_local_storage(self: Self, params: LocalStorageParamsSchema) -> StorageProtocol:
        return LocalStorage(params)


async def get_storage_factory() -> StorageFactoryProtocol:
    return StorageFactoryImpl()


StorageFactory = Annotated[StorageFactoryProtocol, Depends(get_storage_factory)]


async def get_storage_service(storage_factory: StorageFactory, settings: SettingsService) -> StorageProtocol:
    if settings.storage.provider == 's3' and settings.storage.s3 is not None:
        return await storage_factory.make(
            StorageEnum.S3, S3StorageParamsSchema.model_validate(settings.storage.s3.model_dump())
        )
    elif settings.storage.provider == 'local' and settings.storage.dir is not None:
        return await storage_factory.make(StorageEnum.LOCAL, LocalStorageParamsSchema(path=settings.storage.dir))
    raise ValueError(f'Storage {settings.storage.provider} not allowed')


StorageService = Annotated[StorageProtocol, Depends(get_storage_service)]
