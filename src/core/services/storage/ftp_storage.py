"""
Сервис для взаимодействия с ftp.
"""

import contextlib
from pathlib import Path, PosixPath, PurePosixPath
from typing import AsyncIterator, Optional, Union

import aioftp

from .schemas import FtpStorageParamsSchema

PATH_TYPE = Union[str, PurePosixPath, PosixPath]


class FtpStorage:
    def __init__(self, params: FtpStorageParamsSchema) -> None:
        self.params = params
        self.client: Optional[aioftp.Client] = None

    @contextlib.asynccontextmanager
    async def context(self) -> AsyncIterator[aioftp.Client]:
        """
        Метод для создания контекста подключения к ftp.
        """
        async with aioftp.Client.context(
            host=self.params.host,
            port=self.params.port,
            user=self.params.username,
            password=self.params.password,
        ) as client:
            yield client

    async def get_client(self, **kwargs) -> aioftp.Client:
        if self.client is None:
            self.client = aioftp.Client(**kwargs)
            try:
                await self.client.connect(self.params.host, self.params.port)
                await self.client.login(self.params.username, self.params.password)
            except Exception:
                self.client.close()
                raise
        return self.client

    async def quit(self):
        if self.client is not None:
            await self.client.quit()
        self.client = None

    async def exists(self, name: PATH_TYPE, *, client: aioftp.Client) -> bool:
        """
        Функция проверки существования файла.
        """
        client = client or await self.get_client()
        return await client.exists(name)

    async def listdir(
        self, name: PATH_TYPE | None, recursive: bool = False, *, client: aioftp.Client
    ) -> list[PurePosixPath]:
        """
        Получаем список файлов в ftp.
        """
        client = client or await self.get_client()
        return [posix_path async for posix_path, _ in client.list(str(name), recursive=recursive)]

    async def is_file(self, name: str | Path, *, client: aioftp.Client) -> bool:
        client = client or await self.get_client()
        return (await client.stat(name)).get('type') == 'file'

    async def is_dir(self, name: str | Path, *, client: aioftp.Client) -> bool:
        client = client or await self.get_client()
        return (await client.stat(name)).get('type') == 'dir'

    async def read(self, name: str | Path, *, client: aioftp.Client) -> str | bytes:
        client = client or await self.get_client()
        return client.download_stream(name)  # type: ignore

    async def delete(self, name: str | Path, *, client: aioftp.Client) -> None:
        client = client or await self.get_client()
        await client.remove(name)

    async def write(self, name: str | Path, content: str | bytes, *, client: aioftp.Client):
        client = client or await self.get_client()
        if isinstance(content, str):
            content = content.encode('utf-8')
        async with client.upload_stream(name) as stream:  # type: ignore
            await stream.write(content)
