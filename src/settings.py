import os
from os import path
from typing import Annotated, Literal, Optional

from fastapi import Depends
from pydantic import (
    BaseModel,
    RedisDsn,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = (
    'get_settings',
    'Settings',
    'settings',
    'SettingsService',
)


class Db(BaseModel):
    """
    Настройки для подключения к базе данных.
    """

    host: str
    port: int
    user: str
    password: str
    name: str

    provider: str = 'postgresql+psycopg_async'

    @property
    def dsn(self) -> str:
        return f'{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class S3(BaseModel):
    """
    Настройки для S3.
    """

    endpoint: str
    access_key: str
    secret_key: str
    port: int
    bucket: str
    secure: bool = False


class Storage(BaseModel):
    """
    Настройки для хранилища.
    """

    provider: Literal['local', 's3'] = 'local'

    dir: str | None = path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage')
    s3: S3 | None = None


# class Kafka(BaseModel):
#     """
#     Параметры для подключения к провайдеру kafka.
#     """

#     bootstrap_servers: str
#     """
#     Топик записи процессинга.
#     """

#     credentials: Literal['ssl', 'sasl'] | None = None
#     # For ssl
#     cert_file: str | None = None
#     ca_file: str | None = None
#     key_file: str | None = None
#     password: str | None = None
#     # For Sasl
#     broker_username: str | None = None
#     broker_password: str | None = None


class Settings(BaseSettings):
    """
    Настройки модели.
    """

    debug: bool
    base_url: str
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timeout: int = 30  # seconds

    secret_key: str
    redis_dsn: Optional[RedisDsn] = None
    cors_origins: list[str]

    db: Db
    storage: Storage

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )


def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

SettingsService = Annotated[Settings, Depends(get_settings)]
