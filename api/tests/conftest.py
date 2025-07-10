import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Ensure test environment variables are set for a test database if needed
# For example, by loading a .env.test file or setting them here.
# This assumes the main DATABASE_URL from config will be used,
# which might point to the dev DB. For isolated tests, a separate test DB is better.
# os.environ["TESTING"] = "1" # Example flag
# os.environ["DATABASE_URL"] = "postgresql+asyncpg://testuser:testpassword@testdb:5432/testdatabase"

from app.main import app # Main FastAPI application
from app.database import Base, get_db # Base for creating tables, get_db for overriding
from app.core.config import settings # To get DATABASE_URL


# Use a separate database for testing if possible, or ensure clean state.
# For simplicity here, we'll use the configured DB URL but manage schema creation/deletion.
# A more robust setup would use a dedicated test database.
TEST_DATABASE_URL = settings.DATABASE_URL # Replace if you have a specific test DB URL
# If the main DB URL is async, convert it to sync for Alembic metadata operations if needed,
# or use the async engine directly for table creation.
# TEST_DATABASE_URL_SYNC = TEST_DATABASE_URL.replace("+asyncpg", "")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """
    Set up the test database: create all tables before tests run,
    and drop them after tests are done.
    """
    engine = create_async_engine(TEST_DATABASE_URL) # Use the test DB URL
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield # This is where the tests will run

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(setup_test_database) -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture to provide a database session for each test function.
    Ensures the session is rolled back after the test to maintain isolation.
    """
    engine = create_async_engine(TEST_DATABASE_URL)
    AsyncTestingSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
    )
    async with AsyncTestingSessionLocal() as session:
        # Begin a transaction
        await session.begin_nested()
        try:
            yield session
        finally:
            # Rollback the transaction to ensure clean state for next test
            await session.rollback()
            await session.close()
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture to create an AsyncClient for making requests to the FastAPI app.
    Overrides the get_db dependency to use the test database session.
    """
    def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield db_session
        finally:
            # The db_session fixture itself handles commit/rollback/close
            pass

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Clean up dependency override after tests
    del app.dependency_overrides[get_db]


# Fixture to pre-seed data if needed for specific tests
# @pytest.fixture(scope="function")
# async def seed_data_for_test(db_session: AsyncSession):
#     from app.seed import seed_data # Import your seeding function
#     # Adapt seed_data or create a specific test seeder
#     # For example, create a test admin user
#     from app.crud import user as crud_user
#     from app.auth.schemas import UserCreate
#     from app.core.security import get_password_hash

#     admin_user_in = UserCreate(username="testadmin", email="testadmin@example.com", password="testpassword")
#     await crud_user.create(db=db_session, obj_in=admin_user_in)
#     # You might need to commit here if your CRUD operations don't auto-commit in a test context
#     # await db_session.commit()
#     return {"admin_username": "testadmin", "admin_password": "testpassword"}
