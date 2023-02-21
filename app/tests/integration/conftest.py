import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import create_user
from app.auth.router import current_active_user
from app.auth.schemas import UserCreate
from app.database import Base
from app.database.session import get_session
from app.main import app
from app.tests.integration.database import setup_test_db, test_db_async_session_maker, test_db_engine


# From docs: https://pytest-asyncio.readthedocs.io/en/latest/reference/decorators.html
# "All scopes are supported, but if you use a non-function scope you will need
# to redefine the event_loop fixture to have the same or broader scope.
# Async fixtures need the event loop, and so must have the same or narrower scope
# than the event_loop fixture."
@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    await setup_test_db()


@pytest_asyncio.fixture
async def session():
    async with test_db_engine.begin() as conn:
        # will reinit the test db data between each tests
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with test_db_async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture
async def authenticated_client(session: AsyncSession):
    user = await create_user(session, UserCreate(email="user@local.com", password="test"))
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[current_active_user] = lambda: user

    async with AsyncClient(app=app, base_url="http://test.io") as client:
        yield (client, session)
