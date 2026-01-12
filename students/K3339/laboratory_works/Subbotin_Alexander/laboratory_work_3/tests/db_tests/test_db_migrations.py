import pytest
from sqlalchemy import text

from tests.api_tests.constants import ALL_DATABASE_TABLES


@pytest.mark.asyncio(loop_scope="session")
async def test_migrations_applied(db_session):
    """Test all database tables exists"""
    # Select all tables
    result = await db_session.execute(text(
        "SELECT table_name "
        "FROM information_schema.tables "
        "WHERE table_schema = 'public';"
    ))
    # Get all table names
    tables = set(row[0] for row in result)
    # Assert all tables exist
    assert tables == ALL_DATABASE_TABLES
