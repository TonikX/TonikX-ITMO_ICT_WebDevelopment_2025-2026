# Практика 1.1 — Базовый FastAPI + Pydantic

## Цель
Поднять каркас FastAPI, описать Pydantic-модели и сделать CRUD по «временной БД» в памяти.

## Установка и запуск
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Документация — `http://127.0.0.1:8000/docs`.

## Pydantic-модели

```python
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class ExperienceLevel(str, Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class Skill(BaseModel):
    id: int
    name: str
    description: str


class Profession(BaseModel):
    id: int
    title: str
    description: str


class User(BaseModel):
    id: int
    username: str
    level: ExperienceLevel
    profession: Profession              # вложенный объект
    skills: Optional[List[Skill]] = []  # список объектов
```

## Эндпоинты

| Метод   | URL                       | Назначение                |
|---------|---------------------------|---------------------------|
| GET     | `/users_list`             | список пользователей      |
| GET     | `/user/{id}`              | пользователь по id        |
| POST    | `/user`                   | создать                   |
| PUT     | `/user/{id}`              | обновить                  |
| DELETE  | `/user/delete/{id}`       | удалить                   |
| GET     | `/professions_list`       | список профессий          |
| GET     | `/profession/{id}`        | профессия по id           |
| POST    | `/profession`             | создать профессию         |
| DELETE  | `/profession/delete/{id}` | удалить профессию         |

Пример POST с типизированным ответом через `TypedDict`:

```python
@app.post("/user")
def user_create(user: User) -> TypedDict("Response", {"status": int, "data": User}):
    temp_bd.append(user.model_dump())
    return {"status": 200, "data": user}
```

## Итог
Реализован базовый CRUD на временной БД с Pydantic-валидацией, добавлен CRUD для вложенной сущности `Profession`. Готово к переходу на SQLModel/PostgreSQL.
