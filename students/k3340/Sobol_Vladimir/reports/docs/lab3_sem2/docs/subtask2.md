# Подзадача 2 — Вызов парсера из FastAPI

## Что нужно было сделать

Добавить в основное FastAPI-приложение эндпоинт, который принимает
URL от клиента, отправляет запрос парсер-сервису (живёт в отдельном
контейнере) и возвращает ответ.

## Решение

В `main_app/app/routers/parser.py` сделан роутер `/parser` с
синхронным эндпоинтом `POST /parser/parse`:

```python
PARSER_URL = os.getenv("PARSER_URL", "http://parser:8001")

@router.post("/parse")
def parse_sync(payload: ParseRequest):
    try:
        r = requests.post(
            f"{PARSER_URL}/parse",
            json={"url": payload.url},
            timeout=30,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Parser unavailable: {e}")
    return r.json()
```

Особенности:

* `PARSER_URL` берётся из переменной окружения, в compose ему задано
  `http://parser:8001` — Docker DNS резолвит имя сервиса.
* Ошибки сети превращаются в `502 Bad Gateway` для клиента.
* `api` не парсит сам — вся логика парсинга и записи в БД остаётся
  в `parser_app`.

Также добавлен `GET /parser/pages` — общая история распаршенных
страниц (туда же пишут и Celery-таски из подзадачи 3):

```python
@router.get("/pages", response_model=List[ParsedPageRead])
def list_pages(session=Depends(get_session)):
    return session.exec(select(ParsedPage).order_by(ParsedPage.id.desc())).all()
```

## Проверка

```bash
curl -X POST http://localhost:8000/parser/parse \
     -H 'Content-Type: application/json' \
     -d '{"url":"https://example.com/"}'
```

```json
{"id":1,"url":"https://example.com/","title":"Example Domain","source":"http"}
```

```bash
curl http://localhost:8000/parser/pages
```

```json
[{"id":1,"url":"https://example.com/","title":"Example Domain","source":"http","fetched_at":"…"}]
```
