import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.models.review import Review

logger = logging.getLogger(__name__)


async def get_review_by_user_tour(
    db: AsyncSession, 
    user_id: int,
    tour_id: int
) -> Optional[Review]:
    """
    Retrieve a review by user_id and tour_id.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID
        tour_id: Tour ID
    
    Returns:
        Optional[Review]: Review instance if found, None otherwise
    """
    logger.info(f"Fetching review for user ID: {user_id}, tour ID: {tour_id}")
    
    stmt = (
        select(Review)
        .options(selectinload(Review.user))
        .where(Review.user_id == user_id, Review.tour_id == tour_id)
    )
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()
    
    return review
