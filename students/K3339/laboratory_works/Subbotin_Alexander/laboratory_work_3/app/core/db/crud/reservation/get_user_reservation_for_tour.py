import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.reservation import Reservation

logger = logging.getLogger(__name__)


async def get_user_reservation_for_tour(
    db: AsyncSession,
    user_id: int,
    tour_id: int
) -> Optional[Reservation]:
    """
    Check if user has any reservation (regardless of status) for the given tour.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID
        tour_id: Tour ID
    
    Returns:
        Reservation if found, None otherwise
    """
    logger.info(f"Checking existing reservation for user {user_id}, tour {tour_id}")
    
    stmt = select(Reservation).where(
        Reservation.user_id == user_id,
        Reservation.tour_id == tour_id
    )
    result = await db.execute(stmt)
    reservation = result.scalar_one_or_none()
    
    if reservation:
        logger.debug(f"Found existing reservation: {reservation.id} with status: {reservation.status}")
    else:
        logger.debug("No existing reservation found")
    
    return reservation
