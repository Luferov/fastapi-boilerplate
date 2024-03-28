from typing import Self

from src.core.utils.run_in_processpool import run_in_processpool
from src.core.utils.run_in_threadpool import run_in_threadpool


class TestRunInPool:
    def plus(self: Self, a: int, b: int) -> int:
        return a + b

    async def test_processpool(self: Self) -> None:
        """
        Тестируем processpool.
        """
        assert (await run_in_processpool(self.plus, 1, 1)) == 2

    async def test_threadpool(self: Self) -> None:
        assert (await run_in_threadpool(self.plus, 1, 1)) == 2
