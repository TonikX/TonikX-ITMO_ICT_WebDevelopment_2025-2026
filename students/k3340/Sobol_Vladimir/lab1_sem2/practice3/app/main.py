from fastapi import FastAPI

from .connection import init_db
from .routers import auth, users, profiles, skills, projects, teams

app = FastAPI(title="Partner Finder Platform")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(skills.router)
app.include_router(projects.router)
app.include_router(teams.router)


@app.get("/")
def root():
    return {"app": "Partner Finder", "docs": "/docs"}
