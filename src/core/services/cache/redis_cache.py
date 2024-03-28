from __future__ import annotations

from typing import Optional

from fastapi_cache.backends.redis import RedisBackend


class RedisCache(RedisBackend):
    """
    Реализация RedisCache кеша.
    """

    async def incr(self, key: str, amount: int = 1) -> Optional[str]:
        """
        Инкремент значения.
        """
        return await self.redis.incr(key, amount)

    async def decr(self, key: str, amount: int = 1) -> Optional[str]:
        """
        Декремент значения.
        """
        return await self.redis.decr(key, amount)
