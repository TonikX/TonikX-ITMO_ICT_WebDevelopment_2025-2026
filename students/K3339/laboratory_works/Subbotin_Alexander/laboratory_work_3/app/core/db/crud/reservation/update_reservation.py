import logging
from typing import Optional
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.reservation import Reservation

logger = logging.getLogger(__name__)


async def update_reservation(db: AsyncSession, reservation_id: int, reservation_data: dict) -> Optional[Reservation]:
    """
    Update a reservation's information.
    
    Args:
        db: Async SQLAlchemy session
        reservation_id: Reservation ID to update
        reservation_data: Dictionary with fields to update (None values are ignored)
    
    Returns:
        Optional[Reservation]: Updated reservation instance if found, None otherwise
        
    Example:
        >>> update_data = {"guests": 3, "confirmed": True}
        >>> reservation = await update_reservation(db, 1, update_data)
        >>> if reservation:
        ...     print(f"Reservation updated: {reservation.guests} guests, confirmed: {reservation.confirmed}")
    """
    logger.info(f"Updating reservation ID: {reservation_id}")
    
    # Remove None values
    reservation_data = {k: v for k, v in reservation_data.items() if v is not None}
    
    if not reservation_data:
        logger.warning(f"No data to update for reservation ID: {reservation_id}")
        return None
    
    stmt = (
        update(Reservation)
        .where(Reservation.id == reservation_id)
        .values(**reservation_data)
        .returning(Reservation)
    )
    result = await db.execute(stmt)
    await db.commit()
    
    updated_reservation = result.scalar_one_or_none()
    if updated_reservation:
        logger.info(f"Reservation ID {reservation_id} updated successfully")
    else:
        logger.warning(f"Reservation ID {reservation_id} not found")
    
    return updated_reservation
