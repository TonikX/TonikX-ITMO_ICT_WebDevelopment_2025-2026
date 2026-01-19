import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.tour import Tour

logger = logging.getLogger(__name__)


async def get_tour_by_id(db: AsyncSession, tour_id: int) -> Optional[Tour]:
    """
    Retrieve a tour by its ID.
    
    Args:
        db: Async SQLAlchemy session
        tour_id: Tour ID to search for
    
    Returns:
        Optional[Tour]: Tour instance if found, None otherwise
        
    Example:
        >>> tour = await get_tour_by_id(db, 1)
        >>> if tour:
        ...     print(f"{tour.title} in {tour.city}")
    """
    stmt = select(Tour).where(Tour.id == tour_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
