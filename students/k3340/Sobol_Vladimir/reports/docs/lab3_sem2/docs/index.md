# Лабораторная работа №3 (2 семестр)

**Тема:** Упаковка FastAPI-приложения в Docker, отдельный парсер-сервис
и очередь задач Celery + Redis.

## Цель

Научиться:

1. упаковывать FastAPI, PostgreSQL и парсер в Docker и оркестровать их
   через `docker compose`;
2. вызывать парсер из основного приложения по HTTP;
3. ставить задачу парсинга в очередь Celery с брокером Redis и
   выполнять её в отдельном worker-контейнере.

## Архитектура

| Сервис   | Образ / build           | Порт хоста | Назначение |
| -------- | ----------------------- | ---------- | ---------- |
| `db`     | `postgres:16-alpine`    | `5433`     | БД для основного API и для парсера |
| `redis`  | `redis:7-alpine`        | `6379`     | Брокер задач + бэкенд результатов Celery |
| `parser` | `./parser_app`          | `8001`     | FastAPI парсер (`POST /parse`) |
| `api`    | `./main_app`            | `8000`     | Partner Finder из ЛР1 + роутер `/parser` |
| `worker` | `./main_app` (другой CMD) | —        | Celery worker (`celery -A app.tasks.celery_app worker`) |

`api` и `parser` пишут в общую таблицу `parsed_page`. `api` ставит
задачу в Redis, `worker` забирает её и парсит сам (без HTTP-хопа на
parser-сервис, чтобы продемонстрировать чистый паттерн «очередь +
исполнитель»).

```
client ──► api ──► parser  (sync, HTTP)
                   │
                   └──► db

client ──► api ──► redis (queue) ──► worker ──► db   (async, Celery)
```

## Состав отчёта

* [Подзадача 1 — Docker и compose](subtask1.md)
* [Подзадача 2 — Вызов парсера из FastAPI](subtask2.md)
* [Подзадача 3 — Celery + Redis](subtask3.md)
