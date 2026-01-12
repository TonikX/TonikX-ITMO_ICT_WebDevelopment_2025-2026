import logging
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.review import Review

logger = logging.getLogger(__name__)


async def delete_review(db: AsyncSession, review_id: int) -> bool:
    """
    Delete a review by its ID.
    
    Args:
        db: Async SQLAlchemy session
        review_id: Review ID to delete
    
    Returns:
        bool: True if review was deleted, False if review was not found
        
    Example:
        >>> deleted = await delete_review(db, 1)
        >>> if deleted:
        ...     print("Review deleted successfully")
        ... else:
        ...     print("Review not found")
    """
    logger.info(f"Deleting review ID: {review_id}")
    
    stmt = delete(Review).where(Review.id == review_id)
    result = await db.execute(stmt)
    await db.commit()
    
    deleted = result.rowcount > 0
    
    if deleted:
        logger.info(f"Review ID {review_id} deleted successfully")
    else:
        logger.warning(f"Review ID {review_id} not found")
    
    return deleted
