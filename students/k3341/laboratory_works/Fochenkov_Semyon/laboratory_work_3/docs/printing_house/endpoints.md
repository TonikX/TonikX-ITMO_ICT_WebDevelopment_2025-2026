# API Endpoints - Printing House

## Базовый URL

Все API endpoints находятся по адресу: `http://localhost:8000/api/`

## Аутентификация

Все endpoints требуют аутентификации через токены. Используйте заголовок:
```
Authorization: Token <ваш_токен>
```

### Регистрация пользователя

**Endpoint:** `POST /auth/users/`

**Тело запроса:**
```json
{
    "username": "testuser",
    "password": "password123",
    "password_retype": "password123"
}
```

**Ответ:** Информация о созданном пользователе

### Получение токена

**Endpoint:** `POST /auth/token/login/`

**Тело запроса:**
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**Ответ:**
```json
{
    "auth_token": "ваш_токен"
}
```

### Информация о текущем пользователе

**Endpoint:** `GET /auth/users/me/`

**Ответ:** Информация о текущем аутентифицированном пользователе

## Газеты (Newspapers)

### Список всех газет

**Endpoint:** `GET /api/newspapers/`

**Параметры запроса:**
- `page` - номер страницы (для пагинации)
- `page_size` - количество элементов на странице

**Пример ответа:**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Городские вести",
            "publication_index": "GV-001",
            "editor_first_name": "Иван",
            "editor_last_name": "Иванов",
            "editor_middle_name": "Иванович",
            "editor_full_name": "Иванов Иван Иванович",
            "price_per_copy": "25.00"
        }
    ]
}
```

### Детали газеты

**Endpoint:** `GET /api/newspapers/{id}/`

**Пример ответа:**
```json
{
    "id": 1,
    "title": "Городские вести",
    "publication_index": "GV-001",
    "editor_first_name": "Иван",
    "editor_last_name": "Иванов",
    "editor_middle_name": "Иванович",
    "editor_full_name": "Иванов Иван Иванович",
    "price_per_copy": "25.00"
}
```

### Создание газеты

**Endpoint:** `POST /api/newspapers/`

**Тело запроса:**
```json
{
    "title": "Новая газета",
    "publication_index": "NG-999",
    "editor_first_name": "Имя",
    "editor_last_name": "Фамилия",
    "editor_middle_name": "Отчество",
    "price_per_copy": "30.00"
}
```

### Обновление газеты

**Endpoint:** `PUT /api/newspapers/{id}/` или `PATCH /api/newspapers/{id}/`

**Тело запроса:** (аналогично созданию, все поля или только изменяемые)

### Удаление газеты

**Endpoint:** `DELETE /api/newspapers/{id}/`

**Ответ:** 204 No Content

### Газета с вложенными объектами (many-to-many)

**Endpoint:** `GET /api/newspapers/{id}/full_detail/`

**Описание:** Возвращает газету с вложенными тиражами и распределениями. Демонстрирует связь many-to-many через промежуточные модели.

**Пример ответа:**
```json
{
    "id": 1,
    "title": "Городские вести",
    "publication_index": "GV-001",
    "editor_first_name": "Иван",
    "editor_last_name": "Иванов",
    "editor_middle_name": "Иванович",
    "editor_full_name": "Иванов Иван Иванович",
    "price_per_copy": "25.00",
    "printing_runs": [
        {
            "id": 1,
            "newspaper": {
                "id": 1,
                "title": "Городские вести",
                "publication_index": "GV-001",
                ...
            },
            "circulation": 10000
        }
    ],
    "distributions": [
        {
            "id": 1,
            "newspaper": {...},
            "printing_house": {...},
            "quantity": 500
        }
    ]
}
```

### По каким адресам печатаются газеты

**Endpoint:** `GET /api/newspapers/by_name/?name={название}`

**Параметры запроса:**
- `name` - название газеты (обязательно)

**Пример ответа:**
```json
[
    {
        "newspaper": {
            "id": 1,
            "title": "Городские вести",
            ...
        },
        "printing_addresses": [
            {
                "printing_house": "Типография \"Печатный дом\"",
                "address": "г. Москва, ул. Промышленная, д. 15",
                "circulation": 10000
            }
        ]
    }
]
```

### Справка об индексе и цене

**Endpoint:** `GET /api/newspapers/info/?id={id}` или `GET /api/newspapers/info/?name={название}`

**Параметры запроса:**
- `id` - ID газеты (или)
- `name` - название газеты (точное совпадение)

**Пример ответа:**
```json
{
    "title": "Городские вести",
    "publication_index": "GV-001",
    "price_per_copy": "25.00",
    "editor": "Иванов Иван Иванович"
}
```

## Типографии (Printing Houses)

### Список всех типографий

**Endpoint:** `GET /api/printing-houses/`

**Пример ответа:**
```json
{
    "count": 4,
    "results": [
        {
            "id": 1,
            "name": "Типография \"Печатный дом\"",
            "address": "г. Москва, ул. Промышленная, д. 15",
            "is_active": true
        }
    ]
}
```

### Детали типографии

**Endpoint:** `GET /api/printing-houses/{id}/`

### Создание типографии

**Endpoint:** `POST /api/printing-houses/`

**Тело запроса:**
```json
{
    "name": "Новая типография",
    "address": "г. Москва, ул. Примерная, д. 1",
    "is_active": true
}
```

### Обновление типографии

**Endpoint:** `PUT /api/printing-houses/{id}/` или `PATCH /api/printing-houses/{id}/`

### Удаление типографии

**Endpoint:** `DELETE /api/printing-houses/{id}/`

### Типография с вложенными тиражами (one-to-many)

**Endpoint:** `GET /api/printing-houses/{id}/full_detail/`

**Описание:** Возвращает типографию со всеми её тиражами газет. Демонстрирует связь один-ко-многим.

**Пример ответа:**
```json
{
    "id": 1,
    "name": "Типография \"Печатный дом\"",
    "address": "г. Москва, ул. Промышленная, д. 15",
    "is_active": true,
    "printing_runs": [
        {
            "id": 1,
            "newspaper": {
                "id": 1,
                "title": "Городские вести",
                ...
            },
            "circulation": 10000
        }
    ]
}
```

### Редактор газеты с самым большим тиражом

**Endpoint:** `GET /api/printing-houses/{id}/largest_circulation_editor/`

**Описание:** Возвращает информацию о газете с самым большим тиражом в указанной типографии и фамилию её редактора.

**Пример ответа:**
```json
{
    "printing_house": "Типография \"Печатный дом\"",
    "newspaper": "Новости дня",
    "circulation": 15000,
    "editor_last_name": "Петров",
    "editor_full_name": "Петров Петр Петрович"
}
```

### Отчет о работе типографий

**Endpoint:** `GET /api/printing-houses/report/`

**Описание:** Возвращает отчет по каждой активной типографии с детальной информацией о газетах и распределениях.

**Пример ответа:**
```json
[
    {
        "printing_house": {
            "id": 1,
            "name": "Типография \"Печатный дом\"",
            "address": "г. Москва, ул. Промышленная, д. 15",
            "is_active": true
        },
        "total_newspapers": 3,
        "newspapers": [
            {
                "newspaper": "Городские вести",
                "circulation": 10000,
                "distributions": [
                    {
                        "post_office_number": "101001",
                        "post_office_address": "г. Москва, ул. Тверская, д. 1",
                        "quantity": 500
                    }
                ],
                "total_distributed": 900
            }
        ]
    }
]
```

## Почтовые отделения (Post Offices)

### Список всех почтовых отделений

**Endpoint:** `GET /api/post-offices/`

### Детали почтового отделения

**Endpoint:** `GET /api/post-offices/{id}/`

### Создание почтового отделения

**Endpoint:** `POST /api/post-offices/`

**Тело запроса:**
```json
{
    "number": "101004",
    "address": "г. Москва, ул. Новая, д. 10"
}
```

### Обновление почтового отделения

**Endpoint:** `PUT /api/post-offices/{id}/` или `PATCH /api/post-offices/{id}/`

### Удаление почтового отделения

**Endpoint:** `DELETE /api/post-offices/{id}/`

### Почтовое отделение с вложенными распределениями (one-to-many)

**Endpoint:** `GET /api/post-offices/{id}/full_detail/`

**Описание:** Возвращает почтовое отделение со всеми распределениями газет. Демонстрирует связь один-ко-многим.

**Пример ответа:**
```json
{
    "id": 1,
    "number": "101001",
    "address": "г. Москва, ул. Тверская, д. 1",
    "distributions": [
        {
            "id": 1,
            "newspaper": {
                "id": 1,
                "title": "Городские вести",
                ...
            },
            "printing_house": {
                "id": 1,
                "name": "Типография \"Печатный дом\"",
                ...
            },
            "quantity": 500
        }
    ]
}
```

### Почтовые отделения для газет дороже указанной цены

**Endpoint:** `GET /api/post-offices/by_price/?min_price={цена}`

**Параметры запроса:**
- `min_price` - минимальная цена газеты (обязательно, число)

**Пример ответа:**
```json
[
    {
        "post_office": {
            "id": 1,
            "number": "101001",
            "address": "г. Москва, ул. Тверская, д. 1"
        },
        "newspapers": [
            {
                "title": "Новости дня",
                "price": "30.00",
                "quantity": 600
            }
        ]
    }
]
```

### Газеты с количеством меньше заданного

**Endpoint:** `GET /api/post-offices/low_quantity/?max_quantity={количество}`

**Параметры запроса:**
- `max_quantity` - максимальное количество (обязательно, целое число)

**Пример ответа:**
```json
[
    {
        "newspaper": {
            "id": 3,
            "title": "Спортивная жизнь",
            ...
        },
        "post_office_number": "191002",
        "post_office_address": "г. Санкт-Петербург, ул. Садовая, д. 15",
        "quantity": 200
    }
]
```

## Тиражи (Printing Runs)

Тиражи доступны через вложенные объекты в других endpoints. Для прямого доступа можно использовать стандартные CRUD операции через сериализатор.

### Список всех тиражей

**Endpoint:** `GET /api/printing-runs/` (если добавлен в router)

### Детали тиража

**Endpoint:** `GET /api/printing-runs/{id}/` (если добавлен в router)

**Примечание:** Титражи обычно получаются через вложенные объекты в endpoints:
- `GET /api/printing-houses/{id}/full_detail/` - возвращает типографию с тиражами
- `GET /api/newspapers/{id}/full_detail/` - возвращает газету с тиражами

## Распределения (Distributions)

### Список всех распределений

**Endpoint:** `GET /api/distributions/`

### Детали распределения

**Endpoint:** `GET /api/distributions/{id}/`

### Создание распределения

**Endpoint:** `POST /api/distributions/`

**Тело запроса:**
```json
{
    "post_office": 1,
    "newspaper": 1,
    "printing_house": 1,
    "quantity": 500
}
```

### Обновление распределения

**Endpoint:** `PUT /api/distributions/{id}/` или `PATCH /api/distributions/{id}/`

### Удаление распределения

**Endpoint:** `DELETE /api/distributions/{id}/`

### Куда поступает газета по адресу

**Endpoint:** `GET /api/distributions/by_newspaper_and_address/?newspaper_id={id}&address={адрес}`

или

**Endpoint:** `GET /api/distributions/by_newspaper_and_address/?newspaper_name={название}&address={адрес}`

**Параметры запроса:**
- `newspaper_id` - ID газеты (или)
- `newspaper_name` - название газеты (точное совпадение)
- `address` - адрес типографии (обязательно, частичное совпадение)

**Пример ответа:**
```json
{
    "newspaper": {
        "id": 1,
        "title": "Городские вести",
        ...
    },
    "printing_address": "Промышленная",
    "distributions": [
        {
            "post_office": {
                "id": 1,
                "number": "101001",
                "address": "г. Москва, ул. Тверская, д. 1"
            },
            "quantity": 500,
            "printing_house": {
                "id": 1,
                "name": "Типография \"Печатный дом\"",
                ...
            }
        }
    ]
}
```

## Коды ответов

- `200 OK` - успешный запрос
- `201 Created` - успешное создание ресурса
- `204 No Content` - успешное удаление ресурса
- `400 Bad Request` - неверный запрос (отсутствуют обязательные параметры, неверный формат данных)
- `401 Unauthorized` - требуется аутентификация
- `403 Forbidden` - недостаточно прав доступа
- `404 Not Found` - ресурс не найден
- `500 Internal Server Error` - внутренняя ошибка сервера

## Пагинация

По умолчанию все списковые endpoints используют пагинацию с размером страницы 20 элементов.

**Параметры:**
- `page` - номер страницы (по умолчанию 1)
- `page_size` - количество элементов на странице (по умолчанию 20)

**Формат ответа с пагинацией:**
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/newspapers/?page=2",
    "previous": null,
    "results": [...]
}
```

