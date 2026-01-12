import logging
from datetime import datetime
from typing import Optional
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.tour import Tour

logger = logging.getLogger(__name__)


def _strip_timezone(dt) -> datetime:
    """Remove timezone info from datetime to make it naive."""
    if dt is not None and hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def update_tour(db: AsyncSession, tour_id: int, tour_data: dict) -> Optional[Tour]:
    """
    Update a tour's information.
    
    Args:
        db: Async SQLAlchemy session
        tour_id: Tour ID to update
        tour_data: Dictionary with fields to update (None values are ignored)
    
    Returns:
        Optional[Tour]: Updated tour instance if found, None otherwise
        
    Example:
        >>> update_data = {"price": 1200.00, "description": "Updated description"}
        >>> tour = await update_tour(db, 1, update_data)
        >>> if tour:
        ...     print(f"Tour updated: {tour.title} - ${tour.price}")
    """
    logger.info(f"Updating tour ID: {tour_id}")
    
    # Remove None values
    tour_data = {k: v for k, v in tour_data.items() if v is not None}
    
    # Strip timezone from dates to avoid naive/aware datetime mismatch
    if 'start_date' in tour_data:
        tour_data['start_date'] = _strip_timezone(tour_data['start_date'])
    if 'end_date' in tour_data:
        tour_data['end_date'] = _strip_timezone(tour_data['end_date'])
    
    if not tour_data:
        logger.warning(f"No data to update for tour ID: {tour_id}")
        return None
    
    stmt = (
        update(Tour)
        .where(Tour.id == tour_id)
        .values(**tour_data)
        .returning(Tour)
    )
    result = await db.execute(stmt)
    await db.commit()
    
    updated_tour = result.scalar_one_or_none()
    if updated_tour:
        logger.info(f"Tour ID {tour_id} updated successfully")
    else:
        logger.warning(f"Tour ID {tour_id} not found")
    
    return updated_tour
