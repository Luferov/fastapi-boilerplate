"""
Сервис стриминга сообщений.
"""

from typing import Annotated, Protocol, Self

from fastapi import Depends

from src.core.repositories.stream import EntryProcessingEvent, StreamingRepository

from .schemas import EventType

__all__ = ('StreamService',)


class StreamServiceProtocol(Protocol):
    async def send_entry_processing(
        self: Self,
        value: EntryProcessingEvent,
        *,
        key: str | bytes | None = None,
        headers: dict[str, str] | None = None
    ) -> bool:
        """
        Стриминг сообщения в процессинг.
        """
        ...

    async def send_entry_processing_batch(
        self: Self, *values: EntryProcessingEvent, key: str | bytes | None = None, headers: dict[str, str] | None = None
    ) -> bool:
        """
        Стриминг пачки сообщений в процессинг.
        """
        ...


class StreamServiceImpl:
    def __init__(self, repository: StreamingRepository) -> None:
        self.repository = repository

    async def send_entry_processing(
        self: Self,
        value: EntryProcessingEvent,
        *,
        key: str | bytes | None = None,
        headers: dict[str, str] | None = None
    ) -> bool:
        ...
        return await self.repository.send(str(EventType.AUDIO_PROCESSING.value), value, key=key, headers=headers)

    async def send_entry_processing_batch(
        self: Self, *values: EntryProcessingEvent, key: str | bytes | None = None, headers: dict[str, str] | None = None
    ) -> bool:
        return await self.repository.send_batch(str(EventType.AUDIO_PROCESSING.value), *values, key=key)


async def get_stream_service(repository: StreamingRepository) -> StreamServiceProtocol:
    return StreamServiceImpl(repository)


StreamService = Annotated[StreamServiceProtocol, Depends(get_stream_service)]
