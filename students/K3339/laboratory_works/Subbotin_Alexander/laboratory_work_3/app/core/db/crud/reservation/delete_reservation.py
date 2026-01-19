import logging
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.reservation import Reservation

logger = logging.getLogger(__name__)


async def delete_reservation(db: AsyncSession, reservation_id: int) -> bool:
    """
    Delete a reservation by its ID.
    
    Args:
        db: Async SQLAlchemy session
        reservation_id: Reservation ID to delete
    
    Returns:
        bool: True if reservation was deleted, False if reservation was not found
        
    Example:
        >>> deleted = await delete_reservation(db, 1)
        >>> if deleted:
        ...     print("Reservation cancelled successfully")
        ... else:
        ...     print("Reservation not found")
    """
    logger.info(f"Deleting reservation ID: {reservation_id}")
    
    stmt = delete(Reservation).where(Reservation.id == reservation_id)
    result = await db.execute(stmt)
    await db.commit()
    
    deleted = result.rowcount > 0
    
    if deleted:
        logger.info(f"Reservation ID {reservation_id} deleted successfully")
    else:
        logger.warning(f"Reservation ID {reservation_id} not found")
    
    return deleted
