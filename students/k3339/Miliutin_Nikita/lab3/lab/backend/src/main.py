from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.diet import router as diet_router
from src.api.workshop import router as workshop_router
from src.api.cage import router as cage_router
from src.api.breed import router as breed_router
from src.api.breed_diet_season import router as breed_diet_season_router
from src.api.chicken import router as chicken_router
from src.api.chicken_move import router as chicken_move_router
from src.api.employee import router as employee_router
from src.api.employee_cage import router as employee_cage_router
from src.api.auth import router as auth_router
from src.api.analytics import router as analytics_router


app = FastAPI(title="Poultry Farm API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# базовые сущности
app.include_router(diet_router)
app.include_router(workshop_router)
app.include_router(cage_router)
app.include_router(breed_router)
app.include_router(chicken_router)
app.include_router(employee_router)
app.include_router(auth_router)

# связи / события
app.include_router(breed_diet_season_router)
app.include_router(chicken_move_router)
app.include_router(employee_cage_router)
app.include_router(analytics_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
