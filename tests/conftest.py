import asyncio
import os
from typing import Any, Callable, Generator

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope='session')
def prepare_database() -> Callable[[], Generator[Any, Any, Any]]:
    def prepare() -> Generator[Any, Any, Any]:
        os.system('alembic upgrade head')
        # insert mock data
        yield
        os.system('alembic downgrade base')

    return prepare


@pytest.fixture
async def client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
