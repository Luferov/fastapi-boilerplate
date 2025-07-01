"""
Основной модуль для роутов приложения.
"""

from fast_clean.contrib.healthcheck.router import router as healthcheck_router
from fastapi import FastAPI


def apply_routes(app: FastAPI) -> None:
    """
    Применяем роуты приложения.
    """

    app.include_router(healthcheck_router)
