from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.common import models
from src.api.routers import auth, users, posts, images
from src.api.sessions import engine
from src.db.schemas import Base, create_reccomended_func


@asynccontextmanager
async def init_db(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await create_reccomended_func(conn)
    yield


app = FastAPI(lifespan=init_db)
app.include_router(auth.endpoints.router)
app.include_router(users.endpoints.router)
app.include_router(posts.endpoints.router)
app.include_router(images.endpoints.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc) -> JSONResponse:
    content = models.Error(detail=[models.ErrorDetails(msg=exc.detail)])
    return JSONResponse(status_code=exc.status_code, content=content.model_dump())


