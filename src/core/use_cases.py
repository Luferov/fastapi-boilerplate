"""
Модуль, содержащий протокол варианта использования.
"""

from typing import Protocol, TypeVar

UseCaseResultSchemaType = TypeVar('UseCaseResultSchemaType', covariant=True)


class UseCaseProtocol(Protocol[UseCaseResultSchemaType]):
    """
    Протокол варианта использования.
    """

    async def __call__(self) -> UseCaseResultSchemaType:
        """
        Вызываем вариант использования.
        """
        ...
