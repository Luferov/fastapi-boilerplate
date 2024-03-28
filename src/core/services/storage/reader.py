from typing import AsyncIterator, Protocol, Self


class StreamReaderProtocol(Protocol):
    """
    Контракт для потокового чтения.
    """

    async def read(self: Self) -> bytes:
        ...

    def __aiter__(self) -> AsyncIterator[bytes]:
        ...

    async def __anext__(self) -> bytes:
        ...


class StreamReadProtocol(Protocol):
    async def read(self: Self) -> bytes:
        ...


class StreamReader:
    """
    Стриминговое чтение данных.
    """

    def __init__(self, reader: StreamReadProtocol, length: int | None = None) -> None:
        self.reader = reader
        self.length = length if length is not None else -1
        self.current = 0

    async def read(self: Self) -> bytes:
        return await self.reader.read()

    def __aiter__(self: Self) -> AsyncIterator[bytes]:
        return self

    async def __anext__(self) -> bytes:
        data = await self.reader.read()
        if data:
            if self.length == -1:
                return data
            elif self.current < self.length:
                self.current += len(data)
                return data
        raise StopAsyncIteration()
