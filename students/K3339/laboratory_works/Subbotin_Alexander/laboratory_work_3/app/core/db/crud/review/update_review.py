import logging
from typing import Optional
from datetime import datetime
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.review import Review

logger = logging.getLogger(__name__)


async def update_review(db: AsyncSession, review_id: int, review_data: dict) -> Optional[Review]:
    """
    Update a review's information.
    
    Args:
        db: Async SQLAlchemy session
        review_id: Review ID to update
        review_data: Dictionary with fields to update (None values are ignored)
    
    Returns:
        Optional[Review]: Updated review instance if found, None otherwise
        
    Example:
        >>> update_data = {"text": "Updated review text", "rating": 8}
        >>> review = await update_review(db, 1, update_data)
        >>> if review:
        ...     print(f"Review updated: {review.text} - {review.rating}/10")
    """
    logger.info(f"Updating review ID: {review_id}")
    
    # Remove None values
    review_data = {k: v for k, v in review_data.items() if v is not None}
    
    if not review_data:
        logger.warning(f"No data to update for review ID: {review_id}")
        return None
    
    # Set updated_at timestamp
    review_data['updated_at'] = datetime.utcnow()
    
    stmt = (
        update(Review)
        .where(Review.id == review_id)
        .values(**review_data)
        .returning(Review)
    )
    result = await db.execute(stmt)
    await db.commit()
    
    updated_review = result.scalar_one_or_none()
    if updated_review:
        logger.info(f"Review ID {review_id} updated successfully")
    else:
        logger.warning(f"Review ID {review_id} not found")
    
    return updated_review
