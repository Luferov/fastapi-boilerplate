from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.apps.integrations.models import Index


USER_ID = int


class User(SQLAlchemyBaseUserTable[USER_ID], Base):
    """
    Модель пользователя.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    indices: Mapped[list[Index]] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, email={self.email!r})'
