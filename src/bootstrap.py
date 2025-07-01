from collections.abc import AsyncGenerator, Callable, Iterable
from contextlib import asynccontextmanager

from fast_clean.container import ContainerManager
from fast_clean.exceptions import use_exceptions_handlers
from fast_clean.middleware import use_middleware
from fastapi import FastAPI

from .settings import SettingsSchema


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Предварительная инициализация приложения.

    - устанавливаем настройки логгирования
    - устанавливаем настройки кеширования
    - устанавливаем настройки стриминга
    """

    yield

    await ContainerManager.close()



def create_app(use_routes: Iterable[Callable[[FastAPI], None]]) -> FastAPI:
    settings = SettingsSchema() # type: ignore
    app = FastAPI(lifespan=lifespan, docs_url='/docs', openapi_url='/docs.json')
    ContainerManager.init_for_fastapi(app)
    use_middleware(app, settings.cors_origins)
    use_exceptions_handlers(app, settings)

    for use_route in use_routes:
        use_route(app)

    return app
