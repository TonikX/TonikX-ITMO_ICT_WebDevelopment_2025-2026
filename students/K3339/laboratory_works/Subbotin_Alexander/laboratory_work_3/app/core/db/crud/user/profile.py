import logging
from typing import Optional
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.user import UserProfile

logger = logging.getLogger(__name__)


async def create_user_profile(db: AsyncSession, user_id: int, date_of_birth: Optional[datetime] = None) -> UserProfile:
    """
    Create a user profile for a user.
    
    Args:
        db: Async SQLAlchemy session
        user_id: ID of the user to create profile for
        date_of_birth: Optional date of birth
    
    Returns:
        UserProfile: Created user profile instance
        
    Example:
        >>> from datetime import datetime
        >>> profile = await create_user_profile(db, 1, datetime(1990, 1, 1))
        >>> print(profile.user_id)
        1
    """
    logger.info(f"Creating profile for user ID: {user_id}")
    profile = UserProfile(user_id=user_id, date_of_birth=date_of_birth)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    logger.info(f"Profile created successfully for user ID: {user_id}")
    return profile


async def get_user_profile(db: AsyncSession, user_id: int) -> Optional[UserProfile]:
    """
    Retrieve a user's profile by user ID.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID to get profile for
    
    Returns:
        Optional[UserProfile]: UserProfile instance if found, None otherwise
        
    Example:
        >>> profile = await get_user_profile(db, 1)
        >>> if profile:
        ...     print(profile.date_of_birth)
    """
    stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_user_profile(db: AsyncSession, user_id: int, date_of_birth: Optional[datetime] = None) -> Optional[UserProfile]:
    """
    Update a user's profile.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID to update profile for
        date_of_birth: New date of birth
    
    Returns:
        Optional[UserProfile]: Updated profile instance if found, None otherwise
        
    Example:
        >>> from datetime import datetime
        >>> profile = await update_user_profile(db, 1, datetime(1991, 5, 15))
        >>> if profile:
        ...     print(profile.date_of_birth)
    """
    logger.info(f"Updating profile for user ID: {user_id}")
    stmt = (
        update(UserProfile)
        .where(UserProfile.user_id == user_id)
        .values(date_of_birth=date_of_birth)
        .returning(UserProfile)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()
