# Подзадача 3 — Celery + Redis

## Что нужно было сделать

Поднять очередь задач: `Celery` как воркер, `Redis` как брокер. Сделать
эндпоинт, который кладёт парсинг URL в очередь и возвращает ответ
сразу, не дожидаясь выполнения.

## Решение

### Celery-приложение

```python title="main_app/app/tasks/celery_app.py"
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery_app = Celery(
    "partner_finder",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["app.tasks.parse_task"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    task_track_started=True,
)
```

* Брокер — Redis `db=0`, бэкенд результатов — Redis `db=1`.
* `task_track_started=True` — чтобы статус `STARTED` был видимым
  пользователю через `GET /parser/parse-async/{task_id}`.

### Задача

Воркер выполняет работу сам — тянет страницу, парсит и пишет в общую
таблицу `parsed_page` через тот же SQLModel-engine, что и `api`:

```python title="main_app/app/tasks/parse_task.py"
@celery_app.task(name="app.tasks.parse_url", bind=True,
                 max_retries=2, default_retry_delay=5)
def parse_url_task(self, url: str) -> dict:
    try:
        r = requests.get(url, timeout=15,
                         headers={"User-Agent": "lab3-celery/1.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "<no title>"
    except requests.RequestException as exc:
        raise self.retry(exc=exc)

    with Session(engine) as session:
        page = ParsedPage(url=url, title=title, source="celery")
        session.add(page); session.commit(); session.refresh(page)
        return {"id": page.id, "url": page.url, "title": page.title, "source": page.source}
```

* `bind=True` + `self.retry` — автоматический ретрай при сетевых сбоях.
* `source="celery"` помечает строку, чтобы потом легко отличать
  результаты sync- и async-парсинга в `GET /parser/pages`.

### Эндпоинты в API

```python title="main_app/app/routers/parser.py"
@router.post("/parse-async", status_code=202)
def parse_async(payload: ParseRequest):
    task = parse_url_task.delay(payload.url)
    return {"task_id": task.id, "status": "queued"}

@router.get("/parse-async/{task_id}")
def parse_async_status(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    body = {"task_id": task_id, "status": res.status}
    if res.successful():
        body["result"] = res.result
    elif res.failed():
        body["error"] = str(res.result)
    return body
```

* `delay()` сериализует задачу в JSON и кладёт в Redis-очередь.
* HTTP-ответ возвращается мгновенно с `202 Accepted` — пользовательский
  опыт не блокируется тяжёлым парсингом.
* Статус и результат тянутся из бэкенда результатов через
  `AsyncResult`.

### Compose: Redis + worker

```yaml
redis:
  image: redis:7-alpine
  ports: ["6379:6379"]
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 5s

worker:
  build: ./main_app
  command: celery -A app.tasks.celery_app.celery_app worker --loglevel=info --concurrency=2
  environment:
    DB_ADMIN: postgresql+psycopg2://postgres:postgres@db:5432/partners_db
    CELERY_BROKER_URL: redis://redis:6379/0
    CELERY_RESULT_BACKEND: redis://redis:6379/1
  depends_on:
    db: { condition: service_healthy }
    redis: { condition: service_healthy }
    api: { condition: service_started }
```

`worker` использует тот же образ, что и `api` (тот же `Dockerfile`,
тот же код) — меняется только `command`. Это типичный паттерн для
Celery-приложений.

## Проверка

```bash
# 1) ставим задачу
curl -X POST http://localhost:8000/parser/parse-async \
     -H 'Content-Type: application/json' \
     -d '{"url":"https://www.python.org/"}'
# {"task_id":"d2b…","status":"queued"}

# 2) пингуем статус
curl http://localhost:8000/parser/parse-async/d2b…
# {"task_id":"d2b…","status":"STARTED"}
# … через пару секунд:
# {"task_id":"d2b…","status":"SUCCESS","result":{"id":2,"url":"…","title":"Welcome to Python.org","source":"celery"}}

# 3) видим обе записи (http и celery) в общей таблице
curl http://localhost:8000/parser/pages
```

В логах `worker`-контейнера:

```
[INFO/MainProcess] Task app.tasks.parse_url[d2b…] received
[INFO/ForkPoolWorker-1] Task app.tasks.parse_url[d2b…] succeeded in 0.42s
```
