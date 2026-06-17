import time

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from .connection import init_db
from .routers import auth, users, profiles, skills, projects, teams, parser

app = FastAPI(title="Partner Finder Platform (lab3)")


@app.on_event("startup")
def on_startup() -> None:
    last_err: Exception | None = None
    for _ in range(20):
        try:
            init_db()
            return
        except OperationalError as e:
            last_err = e
            time.sleep(1)
    raise RuntimeError(f"DB not ready: {last_err}")


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(skills.router)
app.include_router(projects.router)
app.include_router(teams.router)
app.include_router(parser.router)


@app.get("/")
def root():
    return {"app": "Partner Finder", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
