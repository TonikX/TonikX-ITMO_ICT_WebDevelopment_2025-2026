from fastapi import APIRouter
from src.api.flights import router as flights_router
from src.api.auth import router as auth_router
from src.api.book import router as book_router
from src.api.reviews import router as reviews_router

main_router = APIRouter()

main_router.include_router(reviews_router)
main_router.include_router(flights_router)
main_router.include_router(auth_router)
main_router.include_router(book_router)
