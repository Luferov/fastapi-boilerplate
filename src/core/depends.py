from typing import Annotated

from fastapi import Depends
from starlette.datastructures import MutableHeaders as MutableHeaders

from src.core.services.cache import CacheManager, CacheProtocol
from src.settings import SettingsService


async def get_cache_service(settings: SettingsService) -> CacheProtocol:
    if CacheManager.cache is None:
        await CacheManager.init(settings)
    if CacheManager.cache is not None:
        return CacheManager.cache
    raise ValueError('Cache is not initialize')


CacheService = Annotated[CacheProtocol, Depends(get_cache_service)]
