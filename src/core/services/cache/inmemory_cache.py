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

    async def clear(self, namespace: str | None = None, key: str | None = None) -> int:
        """
        Удаление значений.
        """
        count = 0
        if namespace:
            keys = list(self._store.keys())
            for key in keys:
                assert key is not None
                if key.startswith(namespace) and key in self._store:
                    del self._store[key]
                    count += 1
        elif key and key in self._store:
            del self._store[key]
            count += 1
        return count
