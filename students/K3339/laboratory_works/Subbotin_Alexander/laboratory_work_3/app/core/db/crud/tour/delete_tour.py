import logging
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.tour import Tour

logger = logging.getLogger(__name__)


async def delete_tour(db: AsyncSession, tour_id: int) -> bool:
    """
    Delete a tour by its ID.
    
    Args:
        db: Async SQLAlchemy session
        tour_id: Tour ID to delete
    
    Returns:
        bool: True if tour was deleted, False if tour was not found
        
    Example:
        >>> deleted = await delete_tour(db, 1)
        >>> if deleted:
        ...     print("Tour deleted successfully")
        ... else:
        ...     print("Tour not found")
    """
    logger.info(f"Deleting tour ID: {tour_id}")
    
    stmt = delete(Tour).where(Tour.id == tour_id)
    result = await db.execute(stmt)
    await db.commit()
    
    deleted = result.rowcount > 0
    
    if deleted:
        logger.info(f"Tour ID {tour_id} deleted successfully")
    else:
        logger.warning(f"Tour ID {tour_id} not found")
    
    return deleted
