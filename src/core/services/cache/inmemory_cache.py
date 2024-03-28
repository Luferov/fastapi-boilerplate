from fastapi_cache.backends.inmemory import InMemoryBackend


class InMemoryCache(InMemoryBackend):
    async def incr(self, key: str, amount: int = 1) -> str:
        """
        Инкремент значения.
        """
        v = self._get(key)
        if v is None:
            n_value = str(amount)
            await self.set(key, str(amount))
            return n_value
        n_value = str(int(v.data) + amount)
        await self.set(key, n_value)
        return str(n_value)

    async def decr(self, key: str, amount: int = 1) -> str:
        """
        Декремент значения.
        """
        return await self.incr(key, -amount)
