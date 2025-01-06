import ssl
from typing import TypeAlias

from pydantic import BaseModel

__all__ = (
    'CertificateSchema',
    'make_ssl_context',
)


StrOrBytesPath: TypeAlias = str | bytes  # stable


class CertificateSchema(BaseModel):
    """
    Необходимые файлы для создания SSL контекста.
    """

    ca_file: StrOrBytesPath
    cert_file: StrOrBytesPath
    key_file: StrOrBytesPath
    password: str | None = None


async def make_ssl_context(params: CertificateSchema) -> ssl.SSLContext:
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=params.ca_file)
    ssl_context.load_cert_chain(certfile=params.cert_file, keyfile=params.key_file, password=params.password)
    ssl_context.check_hostname = False
    return ssl_context
