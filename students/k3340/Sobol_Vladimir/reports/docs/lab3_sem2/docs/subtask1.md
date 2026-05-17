# Подзадача 1 — Упаковка в Docker

## Что нужно было сделать

Упаковать FastAPI-приложение из ЛР1 (Partner Finder), базу данных
PostgreSQL и парсер из ЛР2 в Docker-контейнеры и связать их через
`docker compose`.

## Решение

### Парсер как отдельный FastAPI-сервис

Парсер из ЛР2 (`asyncio + aiohttp + BeautifulSoup`) был обёрнут в
маленькое FastAPI-приложение `parser_app/`, которое слушает на порту
`8001` и предоставляет `POST /parse`:

```python title="parser_app/app/main.py"
@app.post("/parse")
def parse(payload: ParseRequest):
    try:
        r = requests.get(payload.url, timeout=15,
                         headers={"User-Agent": "lab3-parser/1.0"})
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "<no title>"
    page = save_page(payload.url, title, source="http")
    return {"id": page.id, "url": page.url, "title": page.title, "source": page.source}
```

`save_page` пишет результат в общую с `api` таблицу `parsed_page`
в PostgreSQL.

### Dockerfile

Оба сервиса (`main_app` и `parser_app`) построены по одному шаблону:

```dockerfile title="main_app/Dockerfile"
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /code

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`gcc + libpq-dev` нужны для `psycopg2-binary` (хотя binary, но на
slim-образе иногда требуется при пересборке колеса).

### docker-compose.yml

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: ${POSTGRES_DB:-partners_db}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports: ["5433:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      retries: 10

  parser:
    build: ./parser_app
    environment:
      DB_ADMIN: postgresql+psycopg2://postgres:postgres@db:5432/partners_db
    depends_on:
      db: { condition: service_healthy }

  api:
    build: ./main_app
    environment:
      DB_ADMIN: postgresql+psycopg2://postgres:postgres@db:5432/partners_db
      PARSER_URL: http://parser:8001
    ports: ["8000:8000"]
    depends_on:
      db: { condition: service_healthy }

volumes:
  pgdata:
```

Важные моменты:

* **Named volume `pgdata`** — БД переживает `docker compose down`.
* **`healthcheck` + `depends_on: condition: service_healthy`** — `api`
  не стартует, пока Postgres реально не отвечает на `pg_isready`.
* **Хостовой порт `5433`** для Postgres — чтобы не конфликтовать с
  локальным Postgres из ЛР1.

### Запуск

```bash
cd lab3_sem2
cp .env.example .env
docker compose up --build
```

Проверить:

```bash
curl http://localhost:8000/health   # {"status":"ok"}
curl http://localhost:8001/health   # {"status":"ok"}
```
