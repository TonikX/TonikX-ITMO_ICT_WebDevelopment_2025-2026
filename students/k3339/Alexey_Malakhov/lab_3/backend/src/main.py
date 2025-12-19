from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import registry
from src.api import main_router
from src.database import engine
from src.models import (
    base,    # noqa: F401
    interaction,
    subscription,
    user,    # noqa: F401
    author,  # noqa: F401
    content  # noqa: F401
)
from src.models.base import Base
from starlette_admin.contrib.sqla import Admin, ModelView


# ВАЖНО: docs_url=None, чтобы FastAPI не создавал свои /docs
app = FastAPI(
    docs_url="/docs"  # Restore default FastAPI docs
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # если есть локальный фронт
        "http://127.0.0.1:3000",
      ],
    allow_credentials=True,      # нужно для куки
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# роуты приложения
app.include_router(main_router, prefix='/api')

# админка
admin = Admin(engine, title="Miracle Admin")

mapper_registry: registry = Base.registry
for mapper in mapper_registry.mappers:
    model = mapper.class_
    admin.add_view(ModelView(model))

admin.mount_to(app)


@app.get("/")
def read_root():
    return {"message": "hello, russia"}


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
