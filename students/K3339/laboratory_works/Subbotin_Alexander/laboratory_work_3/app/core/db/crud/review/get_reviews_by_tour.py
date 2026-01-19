import logging
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.models.review import Review

logger = logging.getLogger(__name__)


async def get_reviews_by_tour(
    db: AsyncSession, 
    tour_id: int,
    limit: int = 100,
    offset: int = 0
) -> Sequence[Review]:
    """
    Retrieve all reviews for a specific tour with pagination.
    
    Args:
        db: Async SQLAlchemy session
        tour_id: Tour ID to get reviews for
        limit: Maximum number of reviews to return (default: 100)
        offset: Number of reviews to skip for pagination (default: 0)
    
    Returns:
        Sequence[Review]: List of review instances with user data eagerly loaded, 
                         ordered by creation date (newest first)
        
    Example:
        >>> reviews = await get_reviews_by_tour(db, tour_id=1, limit=10)
        >>> for review in reviews:
        ...     print(f"{review.user.username}: {review.text} ({review.rating}/10)")
    """
    logger.info(f"Fetching reviews for tour ID: {tour_id} (limit: {limit}, offset: {offset})")
    
    stmt = (
        select(Review)
        .options(selectinload(Review.user))
        .where(Review.tour_id == tour_id)
        .order_by(Review.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()
    
    logger.debug(f"Found {len(reviews)} reviews for tour ID: {tour_id}")
    return reviews
