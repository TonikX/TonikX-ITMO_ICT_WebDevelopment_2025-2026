# Примеры использования Printing House API

## Настройка окружения

Перед началом работы убедитесь, что сервер запущен и вы получили токен аутентификации.

### Получение токена

```bash
curl -X POST http://localhost:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

Ответ:

```json
{
    "auth_token": "ваш_токен_здесь"
}
```

Сохраните токен для использования в последующих запросах.

## Примеры запросов

### Пример 1: Получение списка всех газет

```bash
curl -X GET http://localhost:8000/api/newspapers/ \
  -H "Authorization: Token <ваш_токен>"
```

### Пример 2: Получение газеты с вложенными объектами (many-to-many)

```bash
curl -X GET http://localhost:8000/api/newspapers/1/full_detail/ \
  -H "Authorization: Token <ваш_токен>"
```

Этот запрос демонстрирует связь many-to-many:

- Газета связана с типографиями через PrintingRun
- Газета связана с почтовыми отделениями через Distribution

### Пример 3: Поиск адресов типографий для газеты

```bash
curl -X GET "http://localhost:8000/api/newspapers/by_name/?name=Городские%20вести" \
  -H "Authorization: Token <ваш_токен>"
```

Ответ содержит информацию о газете и список адресов типографий, где она печатается.

### Пример 4: Получение типографии с вложенными тиражами (one-to-many)

```bash
curl -X GET http://localhost:8000/api/printing-houses/1/full_detail/ \
  -H "Authorization: Token <ваш_токен>"
```

Этот запрос демонстрирует связь один-ко-многим: одна типография имеет много тиражей разных газет.

### Пример 5: Редактор газеты с самым большим тиражом

```bash
curl -X GET http://localhost:8000/api/printing-houses/1/largest_circulation_editor/ \
  -H "Authorization: Token <ваш_токен>"
```

Ответ содержит фамилию редактора газеты, которая печатается в указанной типографии самым большим тиражом.

### Пример 6: Отчет о работе типографий

```bash
curl -X GET http://localhost:8000/api/printing-houses/report/ \
  -H "Authorization: Token <ваш_токен>"
```

Отчет содержит для каждой активной типографии:
- Общее количество печатающихся газет
- Детали по каждой газете с тиражем
- Информацию о распределениях в почтовые отделения

### Пример 7: Почтовые отделения для газет дороже указанной цены

```bash
curl -X GET "http://localhost:8000/api/post-offices/by_price/?min_price=30.00" \
  -H "Authorization: Token <ваш_токен>"
```

Ответ содержит список почтовых отделений и газет с ценой выше указанной, которые туда поступают.

### Пример 8: Газеты с количеством меньше заданного

```bash
curl -X GET "http://localhost:8000/api/post-offices/low_quantity/?max_quantity=200" \
  -H "Authorization: Token <ваш_токен>"
```

Ответ содержит список газет с количеством меньше указанного и номера почтовых отделений, куда они поступают.

### Пример 9: Куда поступает газета по адресу типографии

```bash
curl -X GET "http://localhost:8000/api/distributions/by_newspaper_and_address/?newspaper_id=1&address=Промышленная" \
  -H "Authorization: Token <ваш_токен>"
```

Ответ содержит список почтовых отделений, куда поступает указанная газета, печатающаяся по указанному адресу.

### Пример 10: Создание новой газеты

```bash
curl -X POST http://localhost:8000/api/newspapers/ \
  -H "Authorization: Token <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новая газета",
    "publication_index": "NG-999",
    "editor_first_name": "Имя",
    "editor_last_name": "Фамилия",
    "editor_middle_name": "Отчество",
    "price_per_copy": "30.00"
  }'
```

### Пример 11: Создание тиража

```bash
curl -X POST http://localhost:8000/api/printing-runs/ \
  -H "Authorization: Token <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{
    "printing_house": 1,
    "newspaper": 1,
    "circulation": 5000
  }'
```

### Пример 12: Создание распределения

```bash
curl -X POST http://localhost:8000/api/distributions/ \
  -H "Authorization: Token <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{
    "post_office": 1,
    "newspaper": 1,
    "printing_house": 1,
    "quantity": 300
  }'
```

### Пример 13: Обновление цены газеты

```bash
curl -X PATCH http://localhost:8000/api/newspapers/1/ \
  -H "Authorization: Token <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{
    "price_per_copy": "27.50"
  }'
```

### Пример 14: Закрытие типографии

```bash
curl -X PATCH http://localhost:8000/api/printing-houses/4/ \
  -H "Authorization: Token <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false
  }'
```

### Пример 15: Получение почтового отделения с вложенными распределениями (one-to-many)

```bash
curl -X GET http://localhost:8000/api/post-offices/1/full_detail/ \
  -H "Authorization: Token <ваш_токен>"
```

Этот запрос демонстрирует связь один-ко-многим: одно почтовое отделение получает много распределений газет.
