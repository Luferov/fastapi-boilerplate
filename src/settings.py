import os
from os import path
from typing import Annotated, Literal

from fastapi import Depends
from pydantic import BaseModel, Json, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = (
    'get_settings',
    'Settings',
    'settings',
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
    scheme: str = 'public'

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


class Cache(BaseModel):
    """
    Настройки кеша.
    """

    prefix: str = 'boiler-plate'


class JWT(BaseModel):
    """
    Настройки JWT токена.
    """

    token_audience: Json[list[str]]
    token_algorithm: str


class JWTCookie(BaseModel):
    """
    Настройки создания куки с JWT токеном.
    """

    token_lifetime: int
    cookie_name: str
    cookie_max_age: int
    cookie_path: str
    cookie_secure: bool
    cookie_samesite: Literal['lax', 'strict', 'none']


class Settings(BaseSettings):
    """
    Настройки модели.
    """

    debug: bool
    base_url: str
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    secret_key: str
    cors_origins: list[str]

    redis_dsn: RedisDsn

    db: Db
    storage: Storage
    cache: Cache

    jwt: JWT
    jwt_cookie: JWTCookie

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
