import uuid
from typing import Any, Generic, TypeVar

from fastapi import HTTPException, status

from src.core.db import Base

ModelType = TypeVar('ModelType', bound=Base)


class ModelNotFoundException(HTTPException, Generic[ModelType]):
    """
    Исключения не найденной модели.
    """

    def __init__(
        self,
        model: type[ModelType],
        model_id: uuid.UUID | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f'Unable to find the {model.__name__} with id {model_id}.'
                if model_id is not None
                else f'{model.__name__} id not found.'
            ),
            headers=headers,
        )


class PermissionDeniedError(Exception):
    """
    Ошибка, возникающая при недостатке прав для выполнения действия.
    """

    message = 'Недостаточно прав для выполнения действия'


class ModelAlreadyExistsError(Exception):
    """
    Ошибка, возникающая при попытке создать модель с существующим уникальным полем.
    """

    def __init__(self, field: str, message: str, *args: object) -> None:
        super().__init__(*args)
        self.field = field
        self.message = message


class ValidationError(Exception):
    """
    Ошибка валидации.
    """

    def __init__(self, field: str | list[str], message: str, *args: object) -> None:
        super().__init__(*args)
        self.field = field
        self.message = message


class SortingFieldNotFoundError(Exception):
    """
    Ошибка, возникающая при невозможности найти поле для сортировки.
    """

    def __init__(self, field: str, *args: object) -> None:
        super().__init__(*args)
        self.message = f'Не удалось найти поле для сортировки: {field}'


class FileNotFound(HTTPException):
    """
    Исключение если файл не найден.
    """

    def __init__(self, path: str, headers: dict[str, str] | None = None) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f'File {path} not found.', headers=headers)
