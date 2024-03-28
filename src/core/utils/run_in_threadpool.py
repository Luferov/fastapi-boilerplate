"""
Модель запуска тяжелых операций в ThreadPool.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

R = TypeVar('R')
P = ParamSpec('P')


async def run_in_threadpool(fn: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    with ThreadPoolExecutor() as pool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(pool, fn, *args)
