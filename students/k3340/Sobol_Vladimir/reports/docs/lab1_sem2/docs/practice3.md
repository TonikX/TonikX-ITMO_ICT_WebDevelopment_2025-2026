# Практика 1.3 — Alembic, .env, .gitignore, JWT

Финальная версия проекта. Включает требования на **9** и **15 баллов**.

## Структура

```
practice3/
├── alembic.ini
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── .env.example
├── .gitignore
├── requirements.txt
└── app/
    ├── main.py
    ├── connection.py
    ├── models.py
    ├── schemas.py
    ├── auth/
    │   ├── security.py       # bcrypt + JWT encode/decode
    │   └── dependencies.py   # ручная проверка токена
    └── routers/
        ├── auth.py           # register / login / change-password
        ├── users.py          # me / list / get
        ├── profiles.py       # CRUD анкет + M:N skills
        ├── skills.py
        ├── projects.py       # CRUD проектов + вложенные teams/owner
        └── teams.py          # CRUD команд + добавление участников
```

## Подключение к БД из `.env`

`.env`:

```
DB_ADMIN=postgresql://postgres:123@localhost/partners_db
JWT_SECRET=change-me-super-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

`app/connection.py`:

```python
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

db_url = os.getenv("DB_ADMIN")
engine = create_engine(db_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

## Модель данных (7 таблиц)

| Таблица            | Назначение                          | Связи                                         |
|--------------------|-------------------------------------|-----------------------------------------------|
| `User`             | учётная запись                      | 1:1 → Profile, 1:N → Project, M:N → Team      |
| `Profile`          | анкета                              | 1:1 → User, M:N → Skill                       |
| `Skill`            | навык                               | M:N → Profile                                 |
| `ProfileSkillLink` | **ассоциативная**, поле `level`     | Profile ↔ Skill                               |
| `Project`          | проект                              | N:1 → User (owner), 1:N → Team                |
| `Team`             | команда в проекте                   | N:1 → Project, M:N → User                     |
| `TeamMemberLink`   | **ассоциативная**, `role+joined_at` | Team ↔ User                                   |

```python
class ProfileSkillLink(SQLModel, table=True):
    profile_id: Optional[int] = Field(default=None, foreign_key="profile.id", primary_key=True)
    skill_id:   Optional[int] = Field(default=None, foreign_key="skill.id",   primary_key=True)
    level: ExperienceLevel = Field(default=ExperienceLevel.junior)


class TeamMemberLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role: TeamRole = Field(default=TeamRole.member)
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class User(UserDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete", "uselist": False},
    )
    projects: List["Project"] = Relationship(back_populates="owner")
    teams:    List["Team"]    = Relationship(back_populates="members", link_model=TeamMemberLink)
```

## Миграции Alembic

`alembic.ini` оставлен без `sqlalchemy.url` — URL подставляется из `.env` в `migrations/env.py`:

```python
from dotenv import load_dotenv
from sqlmodel import SQLModel
from app.models import *  # регистрируем метаданные моделей

load_dotenv()
config = context.config
db_url = os.getenv("DB_ADMIN")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

target_metadata = SQLModel.metadata
```

Команды:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## JWT-аутентификация

`app/auth/security.py` — генерация и декодирование токенов, хэш паролей:

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, minutes: Optional[int] = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=minutes or JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire, "iat": datetime.utcnow()}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
```

`app/auth/dependencies.py` — **аутентификация по JWT реализована вручную**, без `OAuth2PasswordBearer` и подобных хелперов:

```python
def get_current_user(request: Request, session=Depends(get_session)) -> User:
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(401, "Missing Bearer token")
    token = auth.split(" ", 1)[1].strip()
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")
    username = payload.get("sub")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user
```

## Эндпоинты

### Auth
| Метод | URL                       | Описание                              |
|-------|---------------------------|---------------------------------------|
| POST  | `/auth/register`          | регистрация (email + username + pwd)  |
| POST  | `/auth/login`             | логин, возвращает JWT                 |
| POST  | `/auth/change-password`   | смена пароля (требует токен)          |

### Users
| Метод | URL              | Описание                            |
|-------|------------------|-------------------------------------|
| GET   | `/users`         | список пользователей                |
| GET   | `/users/me`      | информация о текущем пользователе   |
| GET   | `/users/{id}`    | пользователь по id                  |

### Profiles
| Метод  | URL                          | Описание                                 |
|--------|------------------------------|------------------------------------------|
| POST   | `/profiles`                  | создать анкету                           |
| GET    | `/profiles`                  | список                                   |
| GET    | `/profiles/{id}`             | вложенно: skills + user                  |
| PATCH  | `/profiles/{id}`             | обновить (только владелец)               |
| POST   | `/profiles/{id}/skills`      | прикрепить навык с уровнем (M:N + level) |

### Skills
| Метод  | URL              |
|--------|------------------|
| GET    | `/skills`        |
| POST   | `/skills`        |
| DELETE | `/skills/{id}`   |

### Projects
| Метод  | URL                | Описание                                  |
|--------|--------------------|-------------------------------------------|
| GET    | `/projects`        | список                                    |
| GET    | `/projects/{id}`   | вложенно: owner + teams                   |
| POST   | `/projects`        | создать (owner = текущий пользователь)    |
| PATCH  | `/projects/{id}`   | обновить (только владелец)                |
| DELETE | `/projects/{id}`   | удалить (только владелец)                 |

### Teams
| Метод  | URL                       | Описание                                       |
|--------|---------------------------|------------------------------------------------|
| GET    | `/teams`                  | список                                         |
| GET    | `/teams/{id}`             | вложенно: members                              |
| POST   | `/teams`                  | создать (только владелец проекта)              |
| POST   | `/teams/{id}/members`     | добавить участника с ролью (M:N + role+date)   |

## Запуск

```bash
createdb partners_db
cp .env.example .env
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Итог
- 7 таблиц в PostgreSQL через SQLModel, две ассоциативные сущности с доп. полями.
- Полный CRUD с типизированными ответами и вложенными объектами.
- Миграции через Alembic, URL БД берётся из `.env`.
- Регистрация, логин, JWT, ручная проверка токена, bcrypt-хэширование, `/users/me`, `/users`, смена пароля.
