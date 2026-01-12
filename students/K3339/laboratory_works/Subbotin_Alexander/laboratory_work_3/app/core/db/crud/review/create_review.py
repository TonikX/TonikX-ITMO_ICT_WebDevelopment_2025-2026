import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.review import Review

logger = logging.getLogger(__name__)


async def create_review(db: AsyncSession, user_id: int, review_data: dict) -> Review:
    """
    Create a new review for a tour.
    
    Args:
        db: Async SQLAlchemy session
        user_id: ID of the user creating the review
        review_data: Dictionary containing review information (tour_id, text, rating)
    
    Returns:
        Review: Created review instance
        
    Example:
        >>> review_data = {
        ...     "tour_id": 1,
        ...     "text": "Amazing experience!",
        ...     "rating": 9
        ... }
        >>> review = await create_review(db, user_id=5, review_data=review_data)
        >>> print(f"Review created with rating: {review.rating}/10")
    """
    logger.info(f"Creating review for user ID: {user_id}")
    review = Review(user_id=user_id, **review_data)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    logger.info(f"Review created successfully (ID: {review.id})")
    return review
