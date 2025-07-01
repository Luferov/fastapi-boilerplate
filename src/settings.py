from typing import Annotated

from fast_clean.settings import (
    CoreCacheSettingsSchema,
    CoreDbSettingsSchema,
    CoreSettingsSchema,
    CoreStorageSettingsSchema,
)
from pydantic import Field


class SettingsSchema(CoreSettingsSchema):
    """
    Настройки модели.
    """

    cors_origins: Annotated[list[str], Field(default_factory=list)]

    db: CoreDbSettingsSchema
    storage: CoreStorageSettingsSchema
    cache: CoreCacheSettingsSchema

settings = SettingsSchema() # type: ignore
