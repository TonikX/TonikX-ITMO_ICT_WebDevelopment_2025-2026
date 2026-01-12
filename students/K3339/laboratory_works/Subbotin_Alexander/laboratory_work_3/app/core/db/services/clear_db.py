from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def clear_database(session: AsyncSession) -> None:
    """
    Truncates all tables in the public schema (except alembic_version),
    cascading to dependent tables.

    :param session: An instance of AsyncSession to execute the SQL command.
    """
    plpgsql = """
    DO
    $$
    DECLARE
        tbl RECORD;
    BEGIN
        FOR tbl IN
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public' AND tablename <> 'alembic_version'
        LOOP
            EXECUTE format('TRUNCATE TABLE %I CASCADE;', tbl.tablename);
        END LOOP;
    END
    $$;
    """
    # Execute the PL/pgSQL block to truncate all tables
    async with session.begin():
        await session.execute(text(plpgsql))
