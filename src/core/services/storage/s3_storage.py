from __future__ import annotations

import io
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING, AsyncGenerator

import aiohttp
import miniopy_async
from miniopy_async.error import S3Error

from .reader import StreamReader
from .schemas import S3StorageParamsSchema

if TYPE_CHECKING:
    from . import StreamReaderProtocol


class S3Storage:
    def __init__(self, params: S3StorageParamsSchema):
        self.params = params
        self.client = miniopy_async.Minio(
            f'{self.params.endpoint}:{self.params.port}',
            access_key=self.params.access_key,
            secret_key=self.params.secret_key,
            secure=self.params.secure,
        )

        self.__check_exists = False

    @property
    def bucket(self):
        return self.params.bucket

    async def make_bucket(self):
        """
        Проверяем существует ли bucket, создаем если его нет.

        Проверяем один раз.
        """
        if not self.__check_exists:
            result = await self.client.bucket_exists(self.bucket)
            if not result:
                await self.client.make_bucket(self.bucket)
            self.__check_exists = True

    async def exists(self, name: str | Path) -> bool:
        try:
            await self.client.stat_object(self.bucket, str(name))
            return True
        except S3Error:
            return False

    async def listdir(self, name: str | Path) -> list[str]:
        directory: str = str(name) if isinstance(name, Path) else name
        if directory and directory[-1] != '/':
            directory += '/'
        objects = await self.client.list_objects(self.bucket, prefix=directory)
        return [str(obj.object_name) for obj in objects] if objects else []

    async def is_file(self, name: str | Path) -> bool:
        return not await self.is_dir(name)

    async def is_dir(self, name: str | Path) -> bool:
        result = await self.client.stat_object(self.bucket, str(name))
        return result.is_dir

    async def read(self, name: str | Path) -> str | bytes:
        async with aiohttp.ClientSession() as session:
            response = await self.client.get_object(self.bucket, str(name), session)
            return await response.text()

    @asynccontextmanager
    async def stream_read(self, name: str | Path, chunk: int = 1024) -> AsyncGenerator[StreamReaderProtocol, None]:
        async with aiohttp.ClientSession() as session:
            reader = await self.client.get_object(self.bucket, str(name), session)
            yield StreamReader(reader, length=reader.content_length)

    async def stream_write(self, name: str, stream: StreamReaderProtocol, length: int = -1, part_size: int = 0) -> str:
        """
        Загрузка файла на сервер с помощью потока загрузки.
        """
        result = await self.client.put_object(self.bucket, name, stream, length=length, part_size=part_size)
        return result.object_name

    async def write(self, name: str | Path, content: str | bytes):
        content = content.encode('utf-8') if isinstance(content, str) else content
        data = io.BytesIO(content)
        await self.client.put_object(self.bucket, str(name), data, len(content))

    async def delete(self, name: str | Path) -> None:
        await self.client.remove_object(self.bucket, name)
