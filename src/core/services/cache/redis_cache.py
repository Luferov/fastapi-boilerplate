from __future__ import annotations

from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio.client import Redis


class RedisCache(RedisBackend):
    """
    Реализация RedisCache кеша.
    """

    def __init__(self, redis: Redis):
        super().__init__(redis)
        self.redis: Redis

    async def incr(self, key: str, amount: int = 1) -> int | None:
        """
        Инкремент значения.
        """
        return await self.redis.incr(key, amount)

    async def decr(self, key: str, amount: int = 1) -> int | None:
        """
        Декремент значения.
        """
        return await self.redis.decr(key, amount)
