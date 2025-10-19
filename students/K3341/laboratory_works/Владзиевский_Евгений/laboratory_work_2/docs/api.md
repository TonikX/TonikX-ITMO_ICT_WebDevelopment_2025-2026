# API

Краткое описание основных эндпоинтов.

- GET `/conferences` — список конференций (поддерживаются фильтры и пагинация)
- POST `/conferences` — создать конференцию (только админ)
- GET `/conferences/{id}` — детальная информация
- POST `/conferences/{id}/register` — регистрация на выступление (через UI)
- POST `/reviews` — добавить отзыв
- POST `/token` — получить JWT

Примеры curl:

```bash
curl "http://127.0.0.1:8001/conferences?search=ML&page=1&per_page=5"
```

Вы можете вставить примеры JSON-ответов как изображения в `docs/images/api_response_1.png`.
