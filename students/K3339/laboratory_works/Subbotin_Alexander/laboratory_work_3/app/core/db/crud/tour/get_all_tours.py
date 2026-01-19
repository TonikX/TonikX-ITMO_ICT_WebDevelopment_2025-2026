import logging
from typing import Sequence, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.tour import Tour

logger = logging.getLogger(__name__)


async def get_all_tours(
    db: AsyncSession, 
    limit: int = 100, 
    offset: int = 0,
    city: Optional[str] = None
) -> Sequence[Tour]:
    """
    Retrieve tours with optional filtering and pagination.
    
    Args:
        db: Async SQLAlchemy session
        limit: Maximum number of tours to return (default: 100)
        offset: Number of tours to skip for pagination (default: 0)
        city: Optional city filter (case-insensitive partial match)
    
    Returns:
        Sequence[Tour]: List of tour instances
        
    Example:
        >>> # Get all tours
        >>> tours = await get_all_tours(db)
        >>> 
        >>> # Get tours in Paris with pagination
        >>> paris_tours = await get_all_tours(db, limit=10, offset=0, city="Paris")
        >>> for tour in paris_tours:
        ...     print(f"{tour.title} - ${tour.price}")
    """
    logger.info(f"Fetching tours (limit: {limit}, offset: {offset}, city: {city})")
    stmt = select(Tour)
    
    if city:
        stmt = stmt.where(Tour.city.ilike(f"%{city}%"))
    
    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    tours = result.scalars().all()
    
    logger.debug(f"Found {len(tours)} tours")
    return tours
