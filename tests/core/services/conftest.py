from typing import Awaitable, Callable, Literal, Optional

import pytest
from src.core.services.cache import CacheManager, CacheProtocol, get_cache_service
from src.core.services.storage import StorageProtocol, get_storage_factory, get_storage_service


@pytest.fixture
def make_storage_service(settings) -> Callable[[Literal['local', 's3']], Awaitable[StorageProtocol]]:
    async def make_storage(provider: Literal['local', 's3']) -> StorageProtocol:
        settings.storage.provider = provider
        return await get_storage_service(await get_storage_factory(), settings)

    return make_storage


@pytest.fixture
def make_cache_storage(settings) -> Callable[[str], Awaitable[CacheProtocol]]:
    async def make_cache(redis_dsn: Optional[str]) -> CacheProtocol:
        CacheManager.cache = None
        settings.redis_dsn = redis_dsn
        return await get_cache_service(settings)

    return make_cache
