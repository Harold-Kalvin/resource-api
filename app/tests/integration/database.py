import contextlib

import sqlalchemy.exc
from sqlalchemy import text
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import get_settings

test_db_url = get_settings().db_test_url
test_db_name = make_url(test_db_url).database
test_db_engine = create_async_engine(test_db_url)
test_db_async_session_maker = async_sessionmaker(test_db_engine, expire_on_commit=False)


async def setup_test_db():
    # Postgres does not allow to create/drop databases inside a transaction block.
    # But sqlalchemy always tries to run queries in a transaction.
    # A solution to that is to end the open transaction with a commit.
    default_db_engine = create_async_engine(get_settings().db_url, isolation_level="AUTOCOMMIT")

    async with default_db_engine.begin() as conn:
        with contextlib.suppress(sqlalchemy.exc.DBAPIError):
            await conn.execute(text(f"drop database {test_db_name}"))

        with contextlib.suppress(sqlalchemy.exc.ProgrammingError):
            await conn.execute(text(f"create database {test_db_name}"))

        await conn.close()
