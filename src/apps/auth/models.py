from __future__ import annotations

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base

USER_ID = int


class User(SQLAlchemyBaseUserTable[USER_ID], Base):
    """
    Модель пользователя.
    """

    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, email={self.email!r})'
