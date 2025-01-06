"""
Пакет, содержащий сервис для отправки email.
"""

from typing import Annotated, Protocol, Self

from fastapi import Depends
from users.settings import SettingsService

from .smtp import SMTPEmailService


class EmailServiceProtocol(Protocol):
    """
    Протокол сервиса для оправки email.
    """

    async def send(self: Self, to_email: str, message: str) -> None:
        """
        Отправляем email.
        """
        ...


async def get_email_service(settings: SettingsService) -> EmailServiceProtocol:
    """
    Получаем сервис для отправки email.
    """
    return SMTPEmailService(settings)


EmailService = Annotated[EmailServiceProtocol, Depends(get_email_service)]
