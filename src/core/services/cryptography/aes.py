"""
Модуль, содержащий реализацию сервиса криптографии с использованием алгоритма AES.
"""

import base64
import os
from typing import Self

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from src.settings import Settings


class AesCryptographyService:
    """
    Реализация сервиса криптографии с использованием алгоритма AES.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.backend = default_backend()

    async def encrypt(self: Self, data: str) -> str:
        """
        Зашифровываем данные.
        """
        bytes_data = data.encode(encoding='utf-8')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(bytes_data) + padder.finalize()
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + cipher_text).decode('ascii')

    async def decrypt(self: Self, encrypted_data: str) -> str:
        """
        Расшифровываем данные.
        """
        bytes_encrypted_data = base64.b64decode(encrypted_data)
        iv = bytes_encrypted_data[:16]
        cipher_text = bytes_encrypted_data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data.decode(encoding='utf-8')

    @property
    def key(self: Self) -> bytes:
        """
        Ключ длиной в 32 байта.
        """
        key_bytes = self.settings.secret_key.encode()
        if len(key_bytes) > 32:
            return key_bytes[:32]
        if len(key_bytes) < 32:
            diff = 32 - len(key_bytes)
            return key_bytes + b'0' * diff
        return key_bytes
