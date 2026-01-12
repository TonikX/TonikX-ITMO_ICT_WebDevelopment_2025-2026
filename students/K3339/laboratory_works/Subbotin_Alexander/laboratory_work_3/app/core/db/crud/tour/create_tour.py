import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.tour import Tour

logger = logging.getLogger(__name__)


def _strip_timezone(dt) -> datetime:
    """Remove timezone info from datetime to make it naive."""
    if dt is not None and hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_tour(db: AsyncSession, tour_data: dict) -> Tour:
    """
    Create a new tour.
    
    Args:
        db: Async SQLAlchemy session
        tour_data: Dictionary containing tour information (title, agency, description, 
                   start_date, end_date, price, city, payment_terms)
    
    Returns:
        Tour: Created tour instance
        
    Example:
        >>> from datetime import datetime, timedelta
        >>> tour_data = {
        ...     "title": "Paris Adventure",
        ...     "agency": "Dream Tours",
        ...     "description": "Amazing trip to Paris",
        ...     "start_date": datetime.now() + timedelta(days=30),
        ...     "end_date": datetime.now() + timedelta(days=37),
        ...     "price": 1500.00,
        ...     "city": "Paris",
        ...     "payment_terms": "50% upfront"
        ... }
        >>> tour = await create_tour(db, tour_data)
        >>> print(tour.title)
        Paris Adventure
    """
    logger.info(f"Creating tour: {tour_data.get('title')}")
    
    # Strip timezone from dates to avoid naive/aware datetime mismatch
    if 'start_date' in tour_data:
        tour_data['start_date'] = _strip_timezone(tour_data['start_date'])
    if 'end_date' in tour_data:
        tour_data['end_date'] = _strip_timezone(tour_data['end_date'])
    
    tour = Tour(**tour_data)
    db.add(tour)
    await db.commit()
    await db.refresh(tour)
    logger.info(f"Tour created successfully: {tour.title} (ID: {tour.id})")
    return tour
