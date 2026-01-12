import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.reservation import Reservation

logger = logging.getLogger(__name__)


async def get_confirmed_reservation(
    db: AsyncSession,
    user_id: int,
    tour_id: int
) -> Optional[Reservation]:
    """
    Check if user has a confirmed reservation for the given tour.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID
        tour_id: Tour ID
    
    Returns:
        Reservation if found and confirmed, None otherwise
    """
    logger.info(f"Checking confirmed reservation for user {user_id}, tour {tour_id}")
    
    stmt = select(Reservation).where(
        Reservation.user_id == user_id,
        Reservation.tour_id == tour_id,
        Reservation.status == 'confirmed'
    )
    result = await db.execute(stmt)
    reservation = result.scalar_one_or_none()
    
    if reservation:
        logger.debug(f"Found confirmed reservation: {reservation.id}")
    else:
        logger.debug("No confirmed reservation found")
    
    return reservation
