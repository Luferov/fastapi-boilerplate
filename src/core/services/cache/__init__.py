"""
Предоставляемый приложением кеш.

Представлены следующие реализации:
- Redis
- InMemory
"""

from typing import ClassVar, Optional, Protocol, Tuple, cast

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache as cache
from redis import asyncio as aioredis

from src.settings import Settings

from .inmemory_cache import InMemoryCache as InMemoryCache
from .redis_cache import RedisCache as RedisCache

__all__ = (
    'CacheProtocol',
    'CacheManager',
    'cache',
)


class CacheProtocol(Protocol):
    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[str]]:
        """
        Получение значения со сроком жизни.
        """
        ...

    async def set(self, key: str, value: str, expire: Optional[int] = None) -> None:
        """
        Установка значения.
        """
        ...

    async def get(self, key: str) -> Optional[str]:
        """
        Получение значения.
        """
        ...

    async def incr(self, key: str, amount: int = 1) -> str:
        """
        Инкремент значения.
        """
        ...

    async def decr(self, key: str, amount: int = 1) -> str:
        """
        Декремент значения.
        """
        ...

    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        """
        Удаление значений.
        """
        ...


class CacheManager:
    """
    Менеджер контекста для реализации кеширования.
    """

    cache: ClassVar[CacheProtocol | None] = None

    @classmethod
    async def init(cls, settings: Settings):
        if cls.cache is None:
            cache_backend: RedisCache | InMemoryCache
            if settings.redis_dsn is not None:
                redis_client = aioredis.from_url(url=str(settings.redis_dsn))
                cache_backend = RedisCache(redis_client)
            else:
                cache_backend = InMemoryCache()
            FastAPICache.init(cache_backend, prefix=settings.cache.prefix)
            cls.cache = cast(CacheProtocol, cache_backend)
