from fastapi import APIRouter
from src.api.analitycs import router as analytics_router
from src.api.auth import router as auth_router
from src.api.authors import router as authors_router
from src.api.content import router as content_router
from src.api.interactions import router as interactions_router
from src.api.posts import router as posts_router
from src.api.subscriptions import router as subscriptions_router

main_router = APIRouter()
version = '/v1'

main_router.include_router(content_router, prefix=version)
main_router.include_router(posts_router, prefix=version)
main_router.include_router(authors_router, prefix=version)
main_router.include_router(auth_router, prefix=version)
main_router.include_router(interactions_router, prefix=version)
main_router.include_router(subscriptions_router, prefix=version)
main_router.include_router(analytics_router, prefix=version)