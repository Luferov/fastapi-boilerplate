"""
Модуль запуска тяжелых операций в PoolExecutor.
"""

import asyncio
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec('P')
R = TypeVar('R')


async def run_in_processpool(fn: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """
    Запуск функции в отдельном процессе.

    Используем fork в связи с https://github.com/python/cpython/issues/94765.
    """
    kwargs_fn = partial(fn, *args, **kwargs)
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(mp_context=mp.get_context('fork')) as executor:
        return await loop.run_in_executor(executor, kwargs_fn)
