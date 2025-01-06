from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, AsyncGenerator, cast

from aiofiles import open
from aiofiles import os as aos

from .reader import StreamReader
from .schemas import LocalStorageParamsSchema

if TYPE_CHECKING:
    from . import StreamReaderProtocol


class LocalStorage:
    def __init__(self, params: LocalStorageParamsSchema):
        self.work_dir = Path(params.path)
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        self.logger = getLogger(__name__)

    async def exists(self, name: str | Path) -> bool:
        path = self.work_dir / name
        return await aos.path.exists(path)

    async def listdir(self, name: str | Path | None = None) -> list[str]:
        path = self.work_dir
        if name:
            path = path / name
        return await aos.listdir(path)

    async def is_file(self, name: str | Path) -> bool:
        path = self.work_dir / name
        return await aos.path.isfile(path)

    async def is_dir(self, name: str | Path) -> bool:
        path = self.work_dir / name
        return await aos.path.isdir(path)

    async def read(self, name: str | Path) -> str | bytes:
        path = self.work_dir / name
        async with open(path, 'rb') as f:
            return (await f.read()).decode('utf-8')

    @asynccontextmanager
    async def stream_read(self, name: str | Path) -> AsyncGenerator[StreamReaderProtocol, None]:
        path = self.work_dir / name
        async with open(path, 'rb') as f:
            yield StreamReader(f)

    async def stream_write(self, name: str, stream: StreamReaderProtocol, length: int = -1, part_size: int = 0) -> str:
        """
        Загрузка файла на сервер с помощью потока загрузки.
        """
        if length != -1:
            self.logger.warning('Параметр length не используется для LocalStorage.')
        if part_size != 0:
            self.logger.warning('Параметр part_size не используется для LocalStorage.')
        path = self.work_dir / name
        is_co_function = asyncio.iscoroutinefunction(stream.read)
        async with open(path, 'wb') as f:
            data = cast(bytes, await stream.read() if is_co_function else stream.read())
            await f.write(data)
        return str(path)

    async def write(self, name: str | Path, content: str | bytes):
        path = self.work_dir / name
        await aos.makedirs(path.parent, exist_ok=True)

        async with open(path, mode='wb') as f:
            await f.write(content.encode('utf-8') if isinstance(content, str) else content)

    async def delete(self, name: str | Path) -> None:
        path = self.work_dir / name
        await aos.remove(path)
