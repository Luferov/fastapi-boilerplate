from pydantic import BaseModel


class CreateBaseModel(BaseModel):
    """
    Контракт для создания моделей.
    """

    id: int | None = None


class UpdateBaseModel(BaseModel):
    """
    Контракт обновления моделей.
    """

    id: int


class StatusOkSchema(BaseModel):
    status: str = 'ok'
