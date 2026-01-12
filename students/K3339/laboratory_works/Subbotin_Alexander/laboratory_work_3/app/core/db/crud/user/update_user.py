import logging
from typing import Optional
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.user import User
from app.core.settings.security import get_password_hash

logger = logging.getLogger(__name__)


async def update_user(
    db: AsyncSession,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None
) -> Optional[User]:
    """
    Update user's username and/or email.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID to update
        username: New username (optional)
        email: New email (optional)
    
    Returns:
        Optional[User]: Updated user instance if found, None otherwise
    """
    logger.info(f"Updating user ID: {user_id}")
    
    update_data = {}
    if username is not None:
        update_data['username'] = username
    if email is not None:
        update_data['email'] = email
    
    if not update_data:
        # Nothing to update, fetch and return current user
        from app.core.db.crud.user.get_user import get_user_by_id
        return await get_user_by_id(db, user_id)
    
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**update_data)
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    
    updated_user = result.scalar_one_or_none()
    if updated_user:
        logger.info(f"User ID {user_id} updated successfully")
    else:
        logger.warning(f"User ID {user_id} not found for update")
    
    return updated_user


async def update_user_password(
    db: AsyncSession,
    user_id: int,
    new_password: str
) -> Optional[User]:
    """
    Update user's password.
    
    Args:
        db: Async SQLAlchemy session
        user_id: User ID to update
        new_password: New plain text password (will be hashed)
    
    Returns:
        Optional[User]: Updated user instance if found, None otherwise
    """
    logger.info(f"Updating password for user ID: {user_id}")
    
    hashed_password = get_password_hash(new_password)
    
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(hashed_password=hashed_password)
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    
    updated_user = result.scalar_one_or_none()
    if updated_user:
        logger.info(f"Password updated for user ID {user_id}")
    else:
        logger.warning(f"User ID {user_id} not found for password update")
    
    return updated_user
