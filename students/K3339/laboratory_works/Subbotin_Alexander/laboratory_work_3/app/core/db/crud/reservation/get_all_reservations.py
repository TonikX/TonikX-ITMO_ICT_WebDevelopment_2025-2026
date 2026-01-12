import logging
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.models.reservation import Reservation

logger = logging.getLogger(__name__)


async def get_all_reservations(
    db: AsyncSession, 
    user_id: int,
    limit: int = 100,
    offset: int = 0
) -> Sequence[Reservation]:
    """
    Retrieve all reservations for a specific user with pagination.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID to get reservations for
        limit: Maximum number of reservations to return (default: 100)
        offset: Number of reservations to skip for pagination (default: 0)
    
    Returns:
        Sequence[Reservation]: List of reservation instances with tour data eagerly loaded
        
    Example:
        >>> reservations = await get_all_reservations(db, user_id=5, limit=10)
        >>> for res in reservations:
        ...     print(f"Reservation {res.id}: {res.tour.title} - {res.guests} guests")
    """
    logger.info(f"Fetching reservations for user ID: {user_id} (limit: {limit}, offset: {offset})")
    
    stmt = (
        select(Reservation)
        .options(selectinload(Reservation.tour))
        .where(Reservation.user_id == user_id)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    reservations = result.scalars().all()
    
    logger.debug(f"Found {len(reservations)} reservations for user ID: {user_id}")
    return reservations
