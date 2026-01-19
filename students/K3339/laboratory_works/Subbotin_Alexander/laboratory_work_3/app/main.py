import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routers import auth, tours, reservations, reviews
from app.core.database import init_db, close_db
from app.core.logging_config import setup_logging

# Setup logging
setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)


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
