import logging

from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.db.services import *
from . import database_manage_router

logger = logging.getLogger(__name__)


@database_manage_router.post(
    "/clear_database",
    status_code=status.HTTP_200_OK,
    summary="Очистить базу данных от всех данных (кроме таблицы alembic с миграциями)",
)
async def clear_database_endpoint(
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, str]:
    """
    Clears the database of all data (except alembic table).
    """
    await clear_database(session)
    return {"message": "Database cleared successfully."}
