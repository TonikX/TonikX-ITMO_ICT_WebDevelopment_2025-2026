from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import registry
from src.api import main_router
from src.database import engine
from src.models.airlane import Airlane
from src.models.base import Base
from src.models.flight import Flight
from src.models.reservation import Reservation
from src.models.review import Review
from src.models.seat import Seat
from src.models.ticket import Ticket
from src.models.user import User
from starlette_admin.contrib.sqla import Admin, ModelView

templates = Jinja2Templates(directory="src/templates")

app = FastAPI()

# Подключение статики
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/flights", status_code=303)


# Подключение к БД
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Роутеры
app.include_router(main_router)

# Admin панель
admin = Admin(engine, title="My Admin")

mapper_registry: registry = Base.registry
for mapper in mapper_registry.mappers:
    model = mapper.class_
    admin.add_view(ModelView(model))

admin.mount_to(app)
