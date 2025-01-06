from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.loggers import set_logging
from src.core.services.cache import CacheManager
from src.middleware import apply_middleware
from src.router import apply_routes
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Предварительная инициализация приложения.

    - устанавливаем настройки логгирования
    - устанавливаем настройки кеширования
    - устанавливаем настройки стриминга
    """
    set_logging()

    await CacheManager.init(settings)

    # stream_repository = await get_streaming_repository_type()
    # await stream_repository.start(settings.kafka)

    yield

    # await stream_repository.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url='/docs',
        openapi_url='/docs.json',
    )

    app = apply_routes(apply_middleware(app))

    return app
