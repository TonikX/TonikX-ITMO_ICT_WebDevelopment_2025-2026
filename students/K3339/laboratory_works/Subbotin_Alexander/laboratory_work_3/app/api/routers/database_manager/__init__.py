from fastapi import APIRouter

database_manage_router = APIRouter(prefix="/manage_database", tags=["manage_database"])

# Import endpoint modules so that their routes are registered with the router on package import.
from . import clear_database
from . import migrate_tours

__all__ = ["database_manage_router"]
