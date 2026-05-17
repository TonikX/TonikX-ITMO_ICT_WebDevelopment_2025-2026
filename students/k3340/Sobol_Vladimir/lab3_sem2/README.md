# Лабораторная работа №3 (sem2)

**Тема:** Упаковка FastAPI-приложения в Docker, отдельный парсер-сервис и
очередь задач Celery + Redis.

## Архитектура

Пять контейнеров оркестрируются через `docker compose`:

| Сервис   | Порт хоста | Описание |
| -------- | ---------- | -------- |
| `db`     | `5433`     | PostgreSQL 16 (named volume `pgdata`) |
| `redis`  | `6379`     | Брокер задач Celery + хранилище результатов |
| `parser` | `8001`     | Отдельный FastAPI-сервис: `POST /parse` тянет URL, парсит `<title>`, пишет в `parsed_page` |
| `api`    | `8000`     | Основное FastAPI «Partner Finder» из ЛР1 + роутер `/parser` |
| `worker` | —          | Celery-воркер (`celery -A app.tasks.celery_app.celery_app worker`) |

Все сервисы общаются через общую docker-сеть compose. `api` и `parser`
пишут в одну и ту же таблицу `parsed_page`. `api` оркеструет очередь
через Redis, `worker` выполняет фоновую задачу `app.tasks.parse_url`.

## Структура

```
lab3_sem2/
├── docker-compose.yml
├── .env.example
├── main_app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py              # FastAPI + include /parser
│       ├── connection.py        # Postgres engine
│       ├── models.py            # User/Profile/.../ParsedPage
│       ├── schemas.py
│       ├── auth/                # JWT + bcrypt из ЛР1
│       ├── routers/
│       │   ├── auth.py users.py profiles.py skills.py projects.py teams.py
│       │   └── parser.py        # /parser/parse (HTTP) и /parser/parse-async (Celery)
│       └── tasks/
│           ├── celery_app.py    # Celery() c Redis-брокером
│           └── parse_task.py    # @celery_app.task parse_url_task
└── parser_app/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py              # POST /parse  → BeautifulSoup → save_page
        └── db.py                # ParsedPage mapper + engine
```

## Запуск

```bash
cd lab3_sem2
cp .env.example .env
docker compose up --build
```

Когда поднимется:

* Swagger API:    http://localhost:8000/docs
* Swagger Parser: http://localhost:8001/docs

## Проверка

### Подзадача 2 — синхронный вызов парсера (через api → parser)

```bash
curl -X POST http://localhost:8000/parser/parse \
     -H 'Content-Type: application/json' \
     -d '{"url":"https://example.com/"}'
```

Ответ:
```json
{"id":1,"url":"https://example.com/","title":"Example Domain","source":"http"}
```

### Подзадача 3 — асинхронный вызов через Celery

```bash
# 1. ставим задачу в очередь
curl -X POST http://localhost:8000/parser/parse-async \
     -H 'Content-Type: application/json' \
     -d '{"url":"https://www.python.org/"}'
# {"task_id":"abc-…","status":"queued"}

# 2. смотрим статус
curl http://localhost:8000/parser/parse-async/<task_id>
# {"task_id":"…","status":"SUCCESS","result":{...}}
```

### История

```bash
curl http://localhost:8000/parser/pages
```

## Что было сделано

* **Подзадача 1.** Dockerfile-ы для `api` и `parser`, `docker-compose.yml`
  на 5 сервисов, healthchecks и `depends_on: condition: service_healthy`.
  База в named volume, секреты через `.env`.
* **Подзадача 2.** Роутер `app/routers/parser.py`: `POST /parser/parse`
  идёт по HTTP к `http://parser:8001/parse` и возвращает результат
  клиенту.
* **Подзадача 3.** Добавлены сервисы `redis` и `worker`. Эндпоинт
  `POST /parser/parse-async` кладёт задачу в Celery через
  `parse_url_task.delay(url)`. Воркер тянет страницу, парсит и пишет в
  ту же таблицу `ParsedPage`. Статус доступен через
  `GET /parser/parse-async/{task_id}`.
