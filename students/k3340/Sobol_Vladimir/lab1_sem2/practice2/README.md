# Practice 1.2 — SQLModel + PostgreSQL

## Подготовка
```bash
createdb partners_db
pip install -r requirements.txt
uvicorn main:app --reload
```

## Модели
- `Profile` — анкета (1→1 к Profession)
- `Profession` — 1→N к профилям
- `Skill` — M:N к профилям через `ProfileSkillLink` (с доп. полем `level`)

## Связи
- one-to-many: Profession → Profile
- many-to-many: Profile ↔ Skill через ассоциативную сущность с полем `level`

GET `/profile/{id}` возвращает вложенную профессию и список скиллов.
