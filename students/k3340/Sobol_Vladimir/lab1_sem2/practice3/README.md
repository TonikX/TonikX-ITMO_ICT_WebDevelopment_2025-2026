# Practice 1.3 — Alembic, .env, JWT, полный проект

Веб-платформа для поиска партнёров по проектам.

## Установка
```bash
createdb partners_db
cp .env.example .env
pip install -r requirements.txt
```

## Миграции
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```
URL БД подставляется из `.env` (`DB_ADMIN`) через `migrations/env.py`.

## Запуск
```bash
uvicorn app.main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Модель данных (7 таблиц)
- `User` — учётные записи (+ JWT)
- `Profile` — анкета (1:1 с User)
- `Skill` — навыки
- `ProfileSkillLink` — ассоциативная сущность Profile↔Skill, **доп. поле `level`**
- `Project` — проекты (1:N от User)
- `Team` — команды в проекте (1:N от Project)
- `TeamMemberLink` — ассоциативная сущность Team↔User, **доп. поля `role`, `joined_at`**

Связи: one-to-one (User↔Profile), one-to-many (User→Project, Project→Team), many-to-many с ассоциативными сущностями (Profile↔Skill, Team↔User).

## Структура
```
practice3/
├── alembic.ini
├── migrations/
├── .env.example
├── .gitignore
├── requirements.txt
└── app/
    ├── main.py
    ├── connection.py
    ├── models.py
    ├── schemas.py
    ├── auth/
    │   ├── security.py      # хэш паролей, JWT-энкод/декод
    │   └── dependencies.py  # get_current_user — ручная проверка токена
    └── routers/
        ├── auth.py      # /auth/register, /auth/login, /auth/change-password
        ├── users.py     # /users, /users/me, /users/{id}
        ├── profiles.py  # CRUD + прикрепление навыков (M:N с level)
        ├── skills.py
        ├── projects.py  # CRUD, вложенные teams/owner
        └── teams.py     # CRUD + добавление участников с ролью
```

## Эндпоинты

### Auth
- `POST /auth/register` — регистрация
- `POST /auth/login` — выдача JWT
- `POST /auth/change-password` — смена пароля (требует токен)

### Users
- `GET /users` — список
- `GET /users/me` — текущий пользователь (требует токен)
- `GET /users/{id}` — по id

### Profiles
- `POST /profiles` — создать анкету (требует токен)
- `GET /profiles`, `GET /profiles/{id}` — список/детально (с вложенными скиллами и юзером)
- `PATCH /profiles/{id}`
- `POST /profiles/{id}/skills` — прикрепить скилл с уровнем

### Skills
- `GET /skills`, `POST /skills`, `DELETE /skills/{id}`

### Projects
- `GET /projects`, `GET /projects/{id}` (вложенные owner, teams)
- `POST /projects`, `PATCH /projects/{id}`, `DELETE /projects/{id}`

### Teams
- `GET /teams`, `GET /teams/{id}` (вложенные members)
- `POST /teams`
- `POST /teams/{id}/members` — добавить участника с ролью

## JWT
- Токены выдаются методом `POST /auth/login`
- Проверка токена — вручную в `app/auth/dependencies.py::get_current_user`:
  читаем заголовок `Authorization: Bearer <token>`, декодируем через PyJWT,
  достаём `sub`, находим пользователя в БД. Библиотека берёт на себя только
  создание/декодирование JWT и хэш bcrypt (это разрешено по условию).
