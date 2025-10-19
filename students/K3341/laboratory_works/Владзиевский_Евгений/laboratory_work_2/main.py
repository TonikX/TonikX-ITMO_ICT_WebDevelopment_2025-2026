from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel

from app.db import engine
from app.models import *

from app.routes_users import router as users_router
from app.routes_conferences import router as conferences_router
from app.routes_registrations import router as registrations_router
from app.routes_reviews import router as reviews_router
from app.routes_participants import router as participants_router
from app.routes_web import router as web_router
from app.auth import get_password_hash

app = FastAPI(title="Conference Service")

# mount static and templates for the small frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(users_router)
app.include_router(conferences_router)
app.include_router(registrations_router)
app.include_router(reviews_router)
app.include_router(participants_router)
app.include_router(web_router, prefix="/ui")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    # ensure admin exists
    from app.models import User, Role
    from sqlmodel import Session, select
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == 'admin')).first()
        if not existing:
            admin = User(username='admin', display_name='Administrator', role=Role.admin, password_hash=get_password_hash('admin'))
            session.add(admin)
            session.commit()
