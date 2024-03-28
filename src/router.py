"""
Основной модуль для роутов приложения.
"""

from fastapi import FastAPI

from src.apps.auth.router import router as auth_router
from src.apps.healthcheck.router import router as healthcheck_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Применяем роуты приложения.
    """

    app.include_router(auth_router)
    app.include_router(healthcheck_router)
    return app
