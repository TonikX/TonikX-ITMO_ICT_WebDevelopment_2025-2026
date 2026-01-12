import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.user import User
from app.core.settings.security import get_password_hash

logger = logging.getLogger(__name__)


async def create_user(db: AsyncSession, username: str, email: str, password: str, is_admin: bool = False) -> User:
    """
    Create a new user in the database.
    
    Args:
        db: Async SQLAlchemy session
        username: Unique username for the user
        email: Unique email address
        password: Plain text password (will be hashed)
        is_admin: Whether the user is an admin (default: False)
    
    Returns:
        User: Created user instance
        
    Example:
        >>> user = await create_user(db, "john_doe", "john@example.com", "secret123")
        >>> print(user.username)
        john_doe
    """
    logger.info(f"Creating user: {username}")
    hashed_password = get_password_hash(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_admin=is_admin
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    logger.info(f"User created successfully: {username} (ID: {user.id}, is_admin: {is_admin})")
    return user
