from src.settings import get_settings


async def test_settings(settings):
    assert get_settings() == settings, 'Settings do not create from env variables'
    assert settings.storage.provider in ['local', 's3'], f'Provider {settings.storage.provider} not allowed'
    assert isinstance(settings.cors_origins, list), 'CORS_ORIGINS is not list'
    assert settings.db.dsn == 'postgresql+psycopg_async://postgres:1234@localhost:5432/test', 'PG connection is wrong'
