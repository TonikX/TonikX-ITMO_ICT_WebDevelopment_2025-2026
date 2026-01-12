import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.reservation import Reservation

logger = logging.getLogger(__name__)


async def create_reservation(db: AsyncSession, user_id: int, reservation_data: dict) -> Reservation:
    """
    Create a new reservation for a user.
    
    Args:
        db: Async SQLAlchemy session
        user_id: ID of the user making the reservation
        reservation_data: Dictionary containing reservation information (tour_id, guests, notes, confirmed)
    
    Returns:
        Reservation: Created reservation instance
        
    Example:
        >>> reservation_data = {
        ...     "tour_id": 1,
        ...     "guests": 2,
        ...     "notes": "Need vegetarian meals",
        ...     "confirmed": False
        ... }
        >>> reservation = await create_reservation(db, user_id=5, reservation_data=reservation_data)
        >>> print(f"Reservation {reservation.id} created for {reservation.guests} guests")
    """
    logger.info(f"Creating reservation for user ID: {user_id}")
    reservation = Reservation(user_id=user_id, **reservation_data)
    db.add(reservation)
    await db.commit()
    await db.refresh(reservation)
    logger.info(f"Reservation created successfully (ID: {reservation.id})")
    return reservation
