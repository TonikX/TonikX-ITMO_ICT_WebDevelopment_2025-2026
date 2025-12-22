# API endpoints (ЛР3, обновлённые)

Базовый префикс: `/api/` — при регистрации router в `carApp/urls.py`.

Аутентификация
- POST /api/token/  
  Тело: `{ "username": "...", "password": "..." }`  
  Ответ: `{ "access": "...", "refresh": "..." }`

- POST /api/token/refresh/  
  Тело: `{ "refresh": "..." }`  
  Ответ: `{ "access": "..." }`

Основные ресурсы и примеры

Owners
- GET /api/owners/  
  Ответ: список владельцев (возможна пагинация)
- POST /api/owners/  
  Тело: `{ "first_name": "...", "last_name": "...", "date_of_birth": "YYYY-MM-DD", "city": "..." }`
- GET /api/owners/{id}/  
  Детальный вывод включает вложенные объекты:
  - driver_license
  - contacts (OwnerContact[])
  - ownerships (Ownership[] — каждый элемент может содержать сведения о `car`)
  Пример: см. `docs/images/owner_detail_swagger.png`

Cars
- GET /api/cars/
- POST /api/cars/
- GET /api/cars/{id}/  — детально (vin, registration_number, vehicle_model и т.д.)

VehicleModel
- GET /api/vehicle-models/
- POST /api/vehicle-models/

OwnerContact
- GET /api/contacts/
- POST /api/contacts/

Ownership
- GET /api/ownerships/
- POST /api/ownerships/  
  Тело: `{ "owner": <id>, "car": <id>, "date_start": "YYYY-MM-DD", "date_end": "YYYY-MM-DD" }`  
  Валидация: сервер проверяет, что для той же пары owner+car нет пересекающихся периодов. При ошибке вернёт HTTP 400 и сообщение.

InsurancePolicy
- GET /api/insurance/
- POST /api/insurance/  (policy_number unique)

ServiceRecord
- GET /api/services/
- POST /api/services/

Registration
- GET /api/registrations/
- POST /api/registrations/

Примеры curl
- Получить owner detail:
  curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/owners/1/
- Создать ownership:
  curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"owner":1,"car":2,"date_start":"2024-01-01"}' http://127.0.0.1:8000/api/ownerships/

Формат ошибок
- Ошибки валидации: HTTP 400, тело с полями ошибок (DRF default).

Примечание по пагинации
- Если включена пагинация в DRF, ответ списка будет иметь структуру:
  `{ "count": ..., "next": "...", "previous": "...", "results": [ ... ] }`
  Компоненты фронтенда в проекте обрабатывают оба варианта (`res.data.results || res.data`).