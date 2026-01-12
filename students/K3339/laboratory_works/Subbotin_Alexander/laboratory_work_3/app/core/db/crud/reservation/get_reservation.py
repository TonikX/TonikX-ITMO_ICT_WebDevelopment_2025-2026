from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.models.reservation import Reservation


async def get_reservation_by_id(db: AsyncSession, reservation_id: int) -> Optional[Reservation]:
    """
    Retrieve a reservation by its ID with tour data loaded.
    
    Args:
        db: Async SQLAlchemy session
        reservation_id: Reservation ID to search for
    
    Returns:
        Optional[Reservation]: Reservation instance with tour data if found, None otherwise
        
    Example:
        >>> reservation = await get_reservation_by_id(db, 1)
        >>> if reservation:
        ...     print(f"Reservation for {reservation.tour.title}")
    """
    stmt = (
        select(Reservation)
        .options(selectinload(Reservation.tour))
        .where(Reservation.id == reservation_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
