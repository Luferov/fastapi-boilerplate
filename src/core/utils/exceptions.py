from typing import Any, Dict, Generic, Optional, Type, TypeVar

from fastapi import HTTPException, status

from src.core.db import Base

ModelType = TypeVar('ModelType', bound=Base)


class ModelNotFoundException(HTTPException, Generic[ModelType]):
    """
    Исключения не найденной модели.
    """

    def __init__(
        self,
        model: Type[ModelType],
        model_id: int | str | None = None,
        headers: Optional[dict[str, Any]] = None,
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


class FileNotFound(HTTPException):
    """
    Исключение если файл не най.
    """

    def __init__(self, path: str, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f'File {path} not found.', headers=headers)
