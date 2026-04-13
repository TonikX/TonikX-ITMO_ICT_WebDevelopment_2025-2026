# Practice 1.1 — Базовый FastAPI + Pydantic

Тема: платформа поиска партнёров для проектов.

## Запуск
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Эндпоинты
- `GET /users_list` — список пользователей
- `GET /user/{id}` — пользователь по id
- `POST /user` — создать пользователя
- `PUT /user/{id}` — обновить
- `DELETE /user/delete/{id}` — удалить
- CRUD для `/profession*` (вложенный объект)
