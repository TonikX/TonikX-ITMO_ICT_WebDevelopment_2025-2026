from typing import List
from fastapi import FastAPI
from typing_extensions import TypedDict

from models import User, Profession

app = FastAPI(title="Partner Finder — practice 1")

temp_bd = [
    {
        "id": 1,
        "username": "alice",
        "level": "senior",
        "profession": {"id": 1, "title": "Backend", "description": "Python/FastAPI developer"},
        "skills": [
            {"id": 1, "name": "Python", "description": "General-purpose"},
            {"id": 2, "name": "PostgreSQL", "description": "Relational DB"},
        ],
    },
    {
        "id": 2,
        "username": "bob",
        "level": "middle",
        "profession": {"id": 2, "title": "Frontend", "description": "React developer"},
        "skills": [{"id": 3, "name": "React", "description": "UI library"}],
    },
    {
        "id": 3,
        "username": "carol",
        "level": "junior",
        "profession": {"id": 3, "title": "Designer", "description": "UI/UX designer"},
        "skills": [],
    },
]

professions_bd = [
    {"id": 1, "title": "Backend", "description": "Python/FastAPI developer"},
    {"id": 2, "title": "Frontend", "description": "React developer"},
    {"id": 3, "title": "Designer", "description": "UI/UX designer"},
]


@app.get("/")
def hello() -> str:
    return "Hello, Vladimir!"


@app.get("/users_list")
def users_list() -> List[User]:
    return temp_bd


@app.get("/user/{user_id}")
def user_get(user_id: int) -> List[User]:
    return [u for u in temp_bd if u.get("id") == user_id]


@app.post("/user")
def user_create(user: User) -> TypedDict("Response", {"status": int, "data": User}):
    temp_bd.append(user.model_dump())
    return {"status": 200, "data": user}


@app.delete("/user/delete/{user_id}")
def user_delete(user_id: int):
    for i, u in enumerate(temp_bd):
        if u.get("id") == user_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/user/{user_id}")
def user_update(user_id: int, user: User) -> List[User]:
    for i, u in enumerate(temp_bd):
        if u.get("id") == user_id:
            temp_bd[i] = user.model_dump()
    return temp_bd


@app.get("/professions_list")
def professions_list() -> List[Profession]:
    return professions_bd


@app.get("/profession/{prof_id}")
def profession_get(prof_id: int) -> List[Profession]:
    return [p for p in professions_bd if p.get("id") == prof_id]


@app.post("/profession")
def profession_create(profession: Profession) -> TypedDict("Response", {"status": int, "data": Profession}):
    professions_bd.append(profession.model_dump())
    return {"status": 200, "data": profession}


@app.delete("/profession/delete/{prof_id}")
def profession_delete(prof_id: int):
    for i, p in enumerate(professions_bd):
        if p.get("id") == prof_id:
            professions_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}
