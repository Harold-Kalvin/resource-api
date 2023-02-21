import contextlib

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_user_db, get_user_manager
from app.auth.models import User as UserORM
from app.auth.schemas import UserCreate

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(db: AsyncSession, user: UserCreate) -> UserORM:
    async with get_user_db_context(db) as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            return await user_manager.create(user)
