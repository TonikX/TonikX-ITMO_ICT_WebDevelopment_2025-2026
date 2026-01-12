from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.review import Review


async def get_review_by_id(db: AsyncSession, review_id: int) -> Optional[Review]:
    """
    Retrieve a review by its ID.
    
    Args:
        db: Async SQLAlchemy session
        review_id: Review ID to search for
    
    Returns:
        Optional[Review]: Review instance if found, None otherwise
        
    Example:
        >>> review = await get_review_by_id(db, 1)
        >>> if review:
        ...     print(f"Review: {review.text} - Rating: {review.rating}/10")
    """
    stmt = select(Review).where(Review.id == review_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
