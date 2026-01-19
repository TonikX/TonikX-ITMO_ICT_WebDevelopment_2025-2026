import logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator, Any
from app.core.settings.config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

async_session_local = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """
    Dependency for getting async database session.
    
    Yields:
        AsyncSession: SQLAlchemy async session instance
    """
    async with async_session_local() as session:
        yield session


async def init_db():
    """
    Initialize database on application startup.
    
    Creates all tables based on SQLAlchemy models.
    This function is called during the lifespan startup event.
    """
    from app.core.db import Base
    # Import all models to register them in metadata
    from app.core.db.models.user import User, UserProfile
    from app.core.db.models.tour import Tour
    from app.core.db.models.reservation import Reservation
    from app.core.db.models.review import Review
    
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


async def close_db():
    """
    Close database connections on application shutdown.
    
    Disposes of the engine and closes all active connections.
    This function is called during the lifespan shutdown event.
    """
    logger.info("Disposing database engine...")
    await engine.dispose()
    logger.info("Database engine disposed successfully")

