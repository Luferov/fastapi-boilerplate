import io
from typing import Literal, Self

import pytest
from src.core.services.storage.local_storage import LocalStorage
from src.core.services.storage.s3_storage import S3Storage


@pytest.mark.parametrize('provider, storage', [('s3', S3Storage), ('local', LocalStorage)])
async def test_storage_factory(provider: Literal['local', 's3'], storage, make_storage_service):
    s3_storage = await make_storage_service(provider)
    assert isinstance(s3_storage, storage), f'{provider} not implemented'


@pytest.mark.parametrize('provider', ['s3', 'local'])
class TestStorageImplementations:
    async def test_write(self, provider, make_storage_service):
        storage = await make_storage_service(provider)
        path = 'tmp/test.csv'

        await storage.write(path, 'text')
        assert await storage.exists(path) is True

    async def test_read(self, provider, make_storage_service):
        storage = await make_storage_service(provider)
        text_file = 'test.txt'
        await storage.write(text_file, b'some content')

        r = await storage.read(text_file)
        assert r == 'some content'

    async def test_stream_write(self, provider, make_storage_service) -> None:
        """
        Потоковая запись файлов.
        """
        storage = await make_storage_service(provider)
        file_name = 'content.txt'
        text = b'This is example of text content'

        await storage.stream_write(file_name, io.BytesIO(text), length=len(text))

        async with storage.stream_read(file_name) as stream_reader:
            content = await stream_reader.read()
        assert content == text
        await storage.delete(file_name)

    async def test_stream_async_iterable(self: Self, provider, make_storage_service) -> None:
        storage = await make_storage_service(provider)
        file_name = 'content.txt'
        text = b'This is example of text content'
        await storage.stream_write(file_name, io.BytesIO(text), length=len(text))

        buffer = b''
        async with storage.stream_read(file_name) as stream_reader:
            async for data in stream_reader:
                buffer += data

        assert text == buffer
        await storage.delete(file_name)

    async def test_exists(self, provider, make_storage_service):
        storage = await make_storage_service(provider)
        text_file = 'test.txt'
        await storage.write(text_file, b'some content')

        r = await storage.exists(text_file)
        assert r is True
        await storage.delete(text_file)

    async def test_isfile(self, provider, make_storage_service):
        storage = await make_storage_service(provider)
        text_file = 'test.txt'
        await storage.write(text_file, b'some content')

        r = await storage.is_file(text_file)
        assert r is True

    async def test_isdir(self, provider, make_storage_service):
        storage = await make_storage_service(provider)
        text_file = 'test.txt'
        await storage.write(text_file, b'some content')

        r = await storage.is_dir(text_file)
        assert r is False

    async def test_delete(self, provider, make_storage_service):
        storage = await make_storage_service(provider)
        text_file = 'test.txt'
        await storage.write(text_file, b'some content')

        await storage.delete(text_file)
        assert await storage.exists(text_file) is False
