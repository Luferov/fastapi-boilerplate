from typing import Optional

import pytest
from src.core.services.cache.inmemory_cache import InMemoryCache
from src.core.services.cache.redis_cache import RedisCache
from src.settings import settings


@pytest.mark.parametrize('redis_dsn, cache_class', [(None, InMemoryCache), (settings.redis_dsn, RedisCache)])
async def test_cache_factory(redis_dsn: Optional[str], cache_class, make_cache_storage):
    cache_instance = await make_cache_storage(redis_dsn)
    assert isinstance(cache_instance, cache_class), f'{redis_dsn} not implemented'


@pytest.mark.parametrize('redis_dsn', [None, settings.redis_dsn])
class TestCacheProtocol:
    async def test_get_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)
        r_none = await cache_instance.get(key='key.none')
        key = 'key'
        value = 'value_1'
        await cache_instance.set(key, value=value)
        r_val = await cache_instance.get(key)

        assert r_none is None
        assert r_val == value

        await cache_instance.clear(namespace='key')

    async def test_set_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)
        key = 'key'
        value = 'value'
        await cache_instance.set(key, value)
        r_key = await cache_instance.get(key)

        assert r_key == value

        await cache_instance.clear(namespace='key')

    async def test_incr_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)
        key = 'key.incr'
        r_incr_key = await cache_instance.incr(key)

        r_get_key = await cache_instance.get(key)

        assert str(r_incr_key) == r_get_key

        await cache_instance.clear(namespace='key')

    async def test_incr_set_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)
        key = 'key.incr'

        await cache_instance.set(key, value='100')
        r_decr_key = await cache_instance.incr(key)
        r_get_key = await cache_instance.get(key)

        assert str(r_decr_key) == r_get_key

        await cache_instance.clear(namespace='key')

    async def test_decr_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)

        key = 'key.decr'
        r_decr_key = await cache_instance.decr(key=key)
        r_get_key = await cache_instance.get(key=key)

        assert str(r_decr_key) == r_get_key

        await cache_instance.clear(namespace='key')

    async def test_decr_set_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)
        key = 'key'

        await cache_instance.set(key, value='100')
        r_decr_key = await cache_instance.decr(key)
        r_get_key = await cache_instance.get(key)

        assert str(r_decr_key) == r_get_key

        await cache_instance.clear(namespace='key')

    async def test_clean_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)
        key = 'key'
        value = 'value_7'

        await cache_instance.set(key, value)
        assert await cache_instance.get(key) == value

        await cache_instance.clear(key=key)
        r_key = await cache_instance.get(key)

        assert r_key is None

        await cache_instance.clear(namespace='key')

    async def test_get_with_ttl_operation(self, redis_dsn, make_cache_storage):
        cache_instance = await make_cache_storage(redis_dsn)
        key = 'key'
        value = 'value_8'
        await cache_instance.set(key, value)
        ttl, v = await cache_instance.get_with_ttl(key)

        assert ttl in (0, -1)
        assert v == value

        await cache_instance.clear(namespace='key')
