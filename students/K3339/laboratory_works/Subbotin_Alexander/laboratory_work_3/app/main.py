import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routers import auth, tours, reservations, reviews
from app.api.routers.database_manager import database_manage_router
from app.core.database import init_db, close_db, async_session_local
from app.core.logging_config import setup_logging
from app.core.db import crud

# Setup logging
setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default admin credentials
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@touragency.com"
DEFAULT_ADMIN_PASSWORD = "admin123"


async def create_default_admin():
    """Create default admin user if not exists"""
    async with async_session_local() as db:
        existing_admin = await crud.get_user_by_username(db, DEFAULT_ADMIN_USERNAME)
        if not existing_admin:
            logger.info("Creating default admin user...")
            admin = await crud.create_user(
                db,
                username=DEFAULT_ADMIN_USERNAME,
                email=DEFAULT_ADMIN_EMAIL,
                password=DEFAULT_ADMIN_PASSWORD,
                is_admin=True
            )
            await crud.create_user_profile(db, user_id=admin.id)
            logger.info(f"Default admin created: {DEFAULT_ADMIN_USERNAME}")
        else:
            logger.info("Default admin already exists")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events:
    - Startup: Initialize database and create tables
    - Shutdown: Close database connections
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting Tour Agency API...")
    await init_db()
    logger.info("Database initialized successfully")
    
    # Create default admin
    await create_default_admin()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Tour Agency API...")
    await close_db()
    logger.info("Database connections closed")


app = FastAPI(
    title="Tour Agency API",
    description="API for managing tour agency with tour bookings and reviews",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tours.router)
app.include_router(reservations.router)
app.include_router(reviews.router)
app.include_router(database_manage_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API metadata including version and documentation URLs
    """
    logger.info("Root endpoint accessed")
    return {
        "message": "Tour Agency API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring API availability.
    
    Returns:
        dict: Health status of the API
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.core.main:app", host="0.0.0.0", port=8000, reload=True)
