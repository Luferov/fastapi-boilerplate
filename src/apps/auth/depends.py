from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.apps.auth.models import User
from src.core.db import Session


async def get_user_db(session: Session):
    yield SQLAlchemyUserDatabase(session, User)
