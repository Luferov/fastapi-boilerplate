from typing import Annotated

import typer

from src.core.services.cryptography import get_cryptography_service
from src.settings import settings
from src.tools.app import app
from src.tools.utils import typer_async


@app.command(name='encrypt', help='poetry run python manage.py encrypt [data:str]')
@typer_async
async def encrypt(data: Annotated[str, typer.Argument()]):
    cryptography_service = await get_cryptography_service(settings)
    print(await cryptography_service.encrypt(data))


@app.command(
    name='decrypt',
    help='poetry run python manage.py decrypt [data:str]',
)
@typer_async
async def decrypt(data: Annotated[str, typer.Argument()]):
    cryptography_service = await get_cryptography_service(settings)
    print(await cryptography_service.decrypt(data))
