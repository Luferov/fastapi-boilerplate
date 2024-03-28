from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class TimestampMixin:
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.now, server_default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, default=dt.datetime.now, server_default=func.now(), onupdate=dt.datetime.now
    )
