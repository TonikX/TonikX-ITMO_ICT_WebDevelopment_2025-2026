# Лабораторная работа №1 (2 семестр) — FastAPI

**Тема:** веб-платформа для поиска партнёров по проектам.

Платформа позволяет регистрироваться, заводить анкету с навыками и опытом, создавать проекты и собирать команды, добавляя участников с ролями.

## Структура репозитория

Папка лабораторной: [`students/k3340/Sobol_Vladimir/lab1_sem2`](https://github.com/vovasobol1/TonikX-ITMO_ICT_WebDevelopment_2025-2026/tree/main/students/k3340/Sobol_Vladimir/lab1_sem2)

Каждая практика — отдельная папка:

- [practice1](practice1.md) — базовый FastAPI + Pydantic + временная БД
- [practice2](practice2.md) — SQLModel + PostgreSQL, CRUD, связи 1:N и M:N
- [practice3](practice3.md) — Alembic, `.env`, JWT-авторизация, финальный проект

## Стек
- Python 3.10+
- FastAPI + Pydantic
- SQLModel (поверх SQLAlchemy)
- PostgreSQL
- Alembic
- PyJWT, passlib[bcrypt]
- python-dotenv
