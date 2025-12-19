from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api import main_router
from src.database import engine
from src.models.base import Base

from src.models.user import User
from src.models.driver_license import DriverLicense
from src.models.car import Car
from src.models.ownership import Ownership

from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.auth import AdminUser, AuthProvider

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates")

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello from FastAPI"})


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(main_router)


admin = Admin(engine, title="My Admin")

admin.add_view(ModelView(User))
admin.add_view(ModelView(Car))
admin.add_view(ModelView(Ownership))
admin.add_view(ModelView(DriverLicense))

admin.mount_to(app)
