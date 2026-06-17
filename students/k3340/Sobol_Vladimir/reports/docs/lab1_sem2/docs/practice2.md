# Практика 1.2 — SQLModel + PostgreSQL

## Цель
Перейти с временной БД на PostgreSQL через ORM SQLModel, реализовать CRUD и связи **one-to-many** и **many-to-many** с ассоциативной сущностью.

## Подключение к БД

```python
# connection.py
from sqlmodel import SQLModel, Session, create_engine

db_url = "postgresql://postgres:123@localhost/partners_db"
engine = create_engine(db_url, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

В `main.py`:

```python
@app.on_event("startup")
def on_startup() -> None:
    init_db()
```

## Модели

```python
class ProfileSkillLink(SQLModel, table=True):
    profile_id: Optional[int] = Field(default=None, foreign_key="profile.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    level: ExperienceLevel = Field(default=ExperienceLevel.junior)  # доп. поле связи


class Profession(ProfessionDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profiles: List["Profile"] = Relationship(back_populates="profession")


class Skill(SkillDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profiles: List["Profile"] = Relationship(
        back_populates="skills", link_model=ProfileSkillLink
    )


class Profile(ProfileDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="profiles")
    skills: List[Skill] = Relationship(
        back_populates="profiles", link_model=ProfileSkillLink
    )
```

Связи:

- **one-to-many**: `Profession → Profile`
- **many-to-many**: `Profile ↔ Skill` через `ProfileSkillLink` с доп. полем `level`

## Вложенный GET

```python
class ProfileWithAll(ProfileDefault):
    id: int
    profession: Optional[Profession] = None
    skills: List[Skill] = []


@app.get("/profile/{profile_id}", response_model=ProfileWithAll)
def profile_get(profile_id: int, session=Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile
```

## CRUD

| Метод  | URL                                  | Назначение                                |
|--------|--------------------------------------|-------------------------------------------|
| GET    | `/profiles_list`                     | список                                    |
| GET    | `/profile/{id}`                      | детально (с профессией и навыками)        |
| POST   | `/profile`                           | создать                                   |
| PATCH  | `/profile/{id}`                      | частично обновить                         |
| DELETE | `/profile/{id}`                      | удалить                                   |
| GET/POST   | `/professions_list`, `/profession`   | работа с профессиями                  |
| GET/POST/DEL | `/skills_list`, `/skill`, `/skill/{id}` | работа с навыками                  |
| POST   | `/profile/{pid}/skill/{sid}?level=…` | прикрепить навык с указанием уровня (M:N) |

## Итог
Все сущности перенесены в PostgreSQL через SQLModel. GET-запросы профиля возвращают вложенные объекты профессии и список навыков.
