# API: Туры

Endpoints для работы с турами — просмотр, создание, обновление и удаление.

## Получение списка туров

### `GET /tours/`

Получение списка всех доступных туров с поддержкой пагинации и фильтрации.

**Query параметры:**

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| limit | integer | 100 | Количество туров на странице (1-100) |
| offset | integer | 0 | Смещение для пагинации |
| city | string | null | Фильтр по городу (частичное совпадение) |

**Успешный ответ (200 OK):**

```json
[
  {
    "id": 1,
    "title": "Тур в Париж",
    "agency": "Dream Tours",
    "description": "Незабываемое путешествие по столице Франции",
    "start_date": "2025-06-01",
    "end_date": "2025-06-07",
    "price": "1500.00",
    "city": "Париж",
    "payment_terms": "Оплата 50% при бронировании"
  },
  {
    "id": 2,
    "title": "Тур в Рим",
    "agency": "Italy Travel",
    "description": "Исторический Рим за 5 дней",
    "start_date": "2025-07-10",
    "end_date": "2025-07-15",
    "price": "1200.00",
    "city": "Рим",
    "payment_terms": "Полная оплата за 2 недели до начала"
  }
]
```

**Примеры:**

```bash
# Первые 10 туров
curl "http://localhost:8000/tours/?limit=10&offset=0"

# Туры в Париже
curl "http://localhost:8000/tours/?city=Париж"

# Пагинация (вторая страница по 20 туров)
curl "http://localhost:8000/tours/?limit=20&offset=20"
```

---

## Получение тура по ID

### `GET /tours/{id}`

Получение детальной информации о конкретном туре.

**Path параметры:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| id | integer | ID тура |

**Успешный ответ (200 OK):**

```json
{
  "id": 1,
  "title": "Тур в Париж",
  "agency": "Dream Tours",
  "description": "Незабываемое путешествие по столице Франции. Посещение Эйфелевой башни, Лувра, Версаля.",
  "start_date": "2025-06-01",
  "end_date": "2025-06-07",
  "price": "1500.00",
  "city": "Париж",
  "payment_terms": "Оплата 50% при бронировании, остаток за неделю до начала"
}
```

**Ошибки:**

- `404 Not Found` - тур не найден

---

## Создание тура

### `POST /tours/`

Создание нового тура.

**Требуется авторизация:** ✅

**Тело запроса:**

```json
{
  "title": "Тур в Париж",
  "agency": "Dream Tours",
  "description": "Незабываемое путешествие",
  "start_date": "2025-06-01",
  "end_date": "2025-06-07",
  "price": 1500.00,
  "city": "Париж",
  "payment_terms": "Оплата 50% при бронировании"
}
```

**Параметры:**

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| title | string | ✅ | Название тура (макс. 200 символов) |
| agency | string | ✅ | Название агентства (макс. 200 символов) |
| description | string | ✅ | Описание тура |
| start_date | string (date) | ✅ | Дата начала (YYYY-MM-DD) |
| end_date | string (date) | ✅ | Дата окончания (YYYY-MM-DD) |
| price | number | ✅ | Цена (> 0, 2 знака после запятой) |
| city | string | ✅ | Город (макс. 100 символов) |
| payment_terms | string | ❌ | Условия оплаты |

**Успешный ответ (201 Created):**

```json
{
  "id": 1,
  "title": "Тур в Париж",
  "agency": "Dream Tours",
  "description": "Незабываемое путешествие",
  "start_date": "2025-06-01",
  "end_date": "2025-06-07",
  "price": "1500.00",
  "city": "Париж",
  "payment_terms": "Оплата 50% при бронировании"
}
```

**Ошибки:**

- `401 Unauthorized` - требуется авторизация
- `422 Unprocessable Entity` - невалидные данные

**Пример:**

```bash
curl -X POST "http://localhost:8000/tours/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тур в Париж",
    "agency": "Dream Tours",
    "description": "Незабываемое путешествие",
    "start_date": "2025-06-01",
    "end_date": "2025-06-07",
    "price": 1500.00,
    "city": "Париж",
    "payment_terms": "Оплата 50% при бронировании"
  }'
```

---

## Обновление тура

### `PUT /tours/{id}`

Обновление существующего тура.

**Требуется авторизация:** ✅

**Path параметры:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| id | integer | ID тура |

**Тело запроса (все поля опциональны):**

```json
{
  "title": "Обновлённый тур в Париж",
  "price": 1400.00,
  "payment_terms": "Новые условия оплаты"
}
```

**Успешный ответ (200 OK):**

```json
{
  "id": 1,
  "title": "Обновлённый тур в Париж",
  "agency": "Dream Tours",
  "description": "Незабываемое путешествие",
  "start_date": "2025-06-01",
  "end_date": "2025-06-07",
  "price": "1400.00",
  "city": "Париж",
  "payment_terms": "Новые условия оплаты"
}
```

**Ошибки:**

- `401 Unauthorized` - требуется авторизация
- `404 Not Found` - тур не найден
- `422 Unprocessable Entity` - невалидные данные

---

## Удаление тура

### `DELETE /tours/{id}`

Удаление тура из системы.

**Требуется авторизация:** ✅

**Path параметры:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| id | integer | ID тура |

**Успешный ответ (204 No Content):**

Тело ответа пустое.

**Ошибки:**

- `401 Unauthorized` - требуется авторизация
- `404 Not Found` - тур не найден

**Пример:**

```bash
curl -X DELETE "http://localhost:8000/tours/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Полный пример работы с турами

```python
import requests

BASE_URL = "http://localhost:8000"
token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# 1. Создание тура
create_response = requests.post(
    f"{BASE_URL}/tours/",
    headers=headers,
    json={
        "title": "Тур в Токио",
        "agency": "Asia Travel",
        "description": "Современный Токио за неделю",
        "start_date": "2025-09-01",
        "end_date": "2025-09-08",
        "price": 2500.00,
        "city": "Токио",
        "payment_terms": "Полная оплата за месяц"
    }
)
tour_id = create_response.json()["id"]
print(f"Тур создан с ID: {tour_id}")

# 2. Получение списка туров
tours = requests.get(f"{BASE_URL}/tours/").json()
print(f"Всего туров: {len(tours)}")

# 3. Фильтрация по городу
tokyo_tours = requests.get(
    f"{BASE_URL}/tours/",
    params={"city": "Токио"}
).json()
print(f"Туры в Токио: {len(tokyo_tours)}")

# 4. Обновление тура
requests.put(
    f"{BASE_URL}/tours/{tour_id}",
    headers=headers,
    json={"price": 2300.00}
)
print("Цена обновлена")

# 5. Удаление тура
requests.delete(f"{BASE_URL}/tours/{tour_id}", headers=headers)
print("Тур удалён")
```

---

## Рекомендации

!!! tip "Оптимизация"
    - Используйте пагинацию для больших списков
    - Кешируйте список туров на клиенте
    - Применяйте фильтры для уменьшения объёма данных

!!! info "Валидация дат"
    - `end_date` должна быть позже `start_date`
    - Даты в прошлом не рекомендуются
    - Формат даты: ISO 8601 (YYYY-MM-DD)
