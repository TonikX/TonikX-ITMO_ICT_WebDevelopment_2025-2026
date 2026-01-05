# API — список эндпойнтов и примеры

Базовый префикс API: `/api/`

Аутентификация:
- Регистрация (Djoser): `POST /auth/users/`
- Получение JWT-токена: `POST /api/token/`  (получение access/refresh)
- Обновление токена: `POST /api/token/refresh/`
- Заголовок авторизации для запросов: `Authorization: Bearer <ACCESS_TOKEN>`

Схема OpenAPI:
- JSON схема: `GET /api/schema/`
- Swagger UI: `GET /api/docs/swagger/`
- ReDoc: `GET /api/docs/redoc/`

Основные эндпойнты (carApp):

Owners:
- GET `/api/owners/` — список владельцев, в ответе вложены driver_license и ownerships->car
- POST `/api/owners/` — создать владельца (можно вложить driver_license)
  Пример тела (JSON):
  ```json
  {
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "date_of_birth": "1985-05-10",
    "driver_license": {
      "license_number": "DL1001",
      "license_type": "B",
      "issue_date": "2011-01-01"
    }
  }
  ```
- GET `/api/owners/<id>/` — детальная информация о владельце (включая license и машины)
- PUT/PATCH `/api/owners/<id>/` — обновление владельца и/или его license
- DELETE `/api/owners/<id>/` — удаление владельца

Cars:
- GET `/api/cars/` — список автомобилей
- POST `/api/cars/` — создать автомобиль
- GET `/api/cars/<id>/` — информация об автомобиле
- PUT/PATCH `/api/cars/<id>/` — редактирование
- DELETE `/api/cars/<id>/` — удаление

Ownerships:
- POST `/api/ownerships/create/` — создать запись владения (owner id, car id, даты)
  Пример тела:
  ```json
  {
    "owner": 1,
    "car": 2,
    "date_start": "2023-01-01",
    "date_end": null
  }
  ```
  При попытке создать перекрывающееся владение API вернёт ошибку валидации.

Пример успешного ответа GET `/api/owners/1/` (фрагмент):
```json
{
  "id": 1,
  "first_name": "Ivan",
  "last_name": "Ivanov",
  "date_of_birth": "1985-05-10",
  "driver_license": {
    "id": 1,
    "license_number": "DL1001",
    "license_type": "B",
    "issue_date": "2011-01-01"
  },
  "ownerships": [
    {
      "id": 1,
      "car": {
        "id": 1,
        "make": "Toyota",
        "model": "Camry",
        "color": "red",
        "vin": "VIN0001",
        "reg_number": "A111AA"
      },
      "date_start": "2010-01-01",
      "date_end": "2011-01-01"
    }
  ]
}
```

Примечания:
- Для тестирования защищённых эндпойнтов: сначала получите access token, затем в заголовке `Authorization: Bearer <token>` выполняйте запросы.
- Swagger/UI позволяет выпробовать все эндпойнты прямо из браузера.