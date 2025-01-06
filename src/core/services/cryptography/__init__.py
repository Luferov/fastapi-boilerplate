"""
Пакет, содержащий сервис криптографии для шифрования секретных параметров.
"""

from typing import Annotated, Protocol, Self

from fastapi import Depends
from users.settings import SettingsService

from .aes import AesCryptographyService


class CryptographyServiceProtocol(Protocol):
    """
    Протокол сервиса криптографии для шифрования секретных параметров.
    """

    async def encrypt(self: Self, data: str) -> str:
        """
        Зашифровываем данные.
        """
        ...

    async def decrypt(self: Self, encrypted_data: str) -> str:
        """
        Расшифровываем данные.
        """
        ...


async def get_cryptography_service(settings: SettingsService) -> CryptographyServiceProtocol:
    """
    Получаем сервис криптографии.
    """
    return AesCryptographyService(settings)


CryptographyService = Annotated[CryptographyServiceProtocol, Depends(get_cryptography_service)]
