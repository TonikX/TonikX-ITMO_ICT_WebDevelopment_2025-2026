import asyncio
import os
from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.core.database import get_async_session
from app.main import app
from app.core.db.models.base.base import Base
from .constants import NUMBER_OF_PUBLICATION_TO_MIGRATE


@pytest.fixture(scope="session", autouse=True)
def force_event_loop_as_default() -> Generator[None, Any, None]:
    """
    Force usage of a newly created asyncio event loop as default for the entire test session.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield
    loop.close()


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """
    Provide access to the asyncio event loop created by force_event_loop_as_default.
    """
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, Any, None]:
    """
    Launch a PostgreSQL database in Docker using Testcontainers for the entire test session.

    This fixture starts a Postgres container, sets up environment variables for both
    synchronous and asynchronous SQLAlchemy connection URLs, and tears down the container
    after the session ends.

    Yields:
        The started PostgresContainer instance.
    """
    # Initialize a PostgresContainer with the specified Docker image
    postgres_container = PostgresContainer(
        image="postgres:17",
        username="test",
        password="test_password",
        port=5432
    )
    postgres_container.start()

    # Obtain the synchronous connection URL (using psycopg2)
    raw_database_url = postgres_container.get_connection_url()  # Like dialect+driver://user:pass@host:port/db
    raw_scheme, remainder_of_url = raw_database_url.split("://", 1)
    # Extract only the dialect (e.g., 'postgresql') without the driver
    dialect = raw_scheme.split('+')[0]
    async_database_url = f"{dialect}+asyncpg://{remainder_of_url}"
    os.environ["ASYNC_DATABASE_URL"] = async_database_url

    yield postgres_container

    # Stop and remove the container after tests complete
    postgres_container.stop()


@pytest_asyncio.fixture(scope="session")
async def db_engine(postgres_container) -> AsyncEngine:
    """
    Create all the tables for models via Base.metadata.create_all.
    Return async engine to Asyncpg for use in ASYNC tests.
    """
    async_url = os.environ.get("ASYNC_DATABASE_URL")

    engine = create_async_engine(async_url, future=True, echo=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    return engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def migrate_tours(db_engine: AsyncEngine) -> AsyncGenerator[None, Any]:
    params = {
        "clear_database_first": True,
        "migration_limit": NUMBER_OF_PUBLICATION_TO_MIGRATE,
    }

    async_session_maker = sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def _get_test_session() -> AsyncGenerator[AsyncSession, Any]:
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_async_session] = _get_test_session

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
    ) as client:
        resp = await client.post("/manage_database/migration_pipeline", params=params)
        resp.raise_for_status()

    # sanity check
    async with db_engine.connect() as conn:
        total = await conn.scalar(text("SELECT COUNT(*) FROM publication"))
    print(f"Loaded {total} publications into test database.")

    app.dependency_overrides.clear()

    yield


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine, migrate_publications) -> AsyncGenerator[Any, Any]:
    """
    Create a new database session for each test function with nested transactions.

    This fixture:
    - Opens an async connection and begins a top-level transaction.
    - Creates a sessionmaker bound to the connection using AsyncSession.
    - Begins a nested (SAVEPOINT) transaction for test isolation.
    - Rolls back to the savepoint and closes all resources after the test.

    Yields:
        An AsyncSession instance for database operations within a test.
    """
    # Connect and start a transaction
    connection = await db_engine.connect()
    top_level_transaction = await connection.begin()

    # Configure sessionmaker for AsyncSession
    async_session_local = sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = async_session_local()

    # Begin a nested transaction (SAVEPOINT) for test isolation
    await session.begin_nested()
    try:
        yield session
    finally:
        # Roll back to the nested savepoint and then the top-level transaction
        await session.rollback()
        await top_level_transaction.rollback()
        await session.close()
        await connection.close()


@pytest_asyncio.fixture(scope="function")
def override_get_async_session(db_session) -> Generator[None, Any, None]:
    """
    Overrides the get_async_session dependency in FastAPI to use the test db_session.
    This fixture runs before the client fixture and ensures the override is active.
    """
    # Set the override
    app.dependency_overrides[get_async_session] = lambda: db_session
    yield
    # Clear the override after the test
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def client(override_get_async_session) -> AsyncGenerator[AsyncClient, Any]:
    """
    Provide an AsyncClient for testing FastAPI endpoints with dependency override.

    This fixture:
    - Depends on `override_get_async_session` to ensure the DB dependency is set.
    - Yields a httpx.AsyncClient configured with ASGITransport.

    Args:
        override_get_async_session: The fixture that sets up the database session override.

    Yields:
        An httpx.AsyncClient instance for making test requests.
    """
    # Initialize the AsyncClient with ASGI transport
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as async_client:
        yield async_client

