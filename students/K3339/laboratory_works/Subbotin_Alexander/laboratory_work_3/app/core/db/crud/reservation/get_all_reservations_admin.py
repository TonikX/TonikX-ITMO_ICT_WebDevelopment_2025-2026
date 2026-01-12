import logging
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.models.reservation import Reservation

logger = logging.getLogger(__name__)


async def get_all_reservations_admin(
    db: AsyncSession, 
    limit: int = 100,
    offset: int = 0,
    status: str | None = None
) -> Sequence[Reservation]:
    """
    Retrieve all reservations for admin with pagination and optional filter.
    
    Args:
        db: Async SQLAlchemy session
        limit: Maximum number of reservations to return (default: 100)
        offset: Number of reservations to skip for pagination (default: 0)
        status: Filter by status (pending/confirmed/rejected, None = all)
    
    Returns:
        Sequence[Reservation]: List of reservation instances with tour and user data
    """
    logger.info(f"Admin fetching all reservations (limit: {limit}, offset: {offset}, status: {status})")
    
    stmt = (
        select(Reservation)
        .options(selectinload(Reservation.tour), selectinload(Reservation.user))
        .order_by(Reservation.created_at.desc())
    )
    
    if status is not None:
        stmt = stmt.where(Reservation.status == status)
    
    stmt = stmt.limit(limit).offset(offset)
    
    result = await db.execute(stmt)
    reservations = result.scalars().all()
    
    logger.debug(f"Found {len(reservations)} reservations")
    return reservations
