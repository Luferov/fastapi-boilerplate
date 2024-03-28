from pydantic import BaseModel


class S3StorageParamsSchema(BaseModel):
    """
    Параметры настроек для S3Storage.
    """

    endpoint: str
    access_key: str
    secret_key: str
    port: int
    bucket: str
    secure: bool = False


class LocalStorageParamsSchema(BaseModel):
    """
    Параметры настроек для LocalStorage.
    """

    path: str


class FtpStorageParamsSchema(BaseModel):
    """
    Параметры настроек для FtpStorage.
    """

    host: str
    port: int
    username: str
    password: str
